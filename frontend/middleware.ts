import { NextRequest, NextResponse } from 'next/server';
import { decodeJwt } from 'jose';
import { jwtCookieName } from './lib/config';

function resolveRole(token?: string) {
  if (!token) return null;
  try {
    const decoded = decodeJwt(token) as { role?: string; exp?: number };
    if (decoded.exp && decoded.exp * 1000 < Date.now()) {
      return null;
    }
    return decoded.role ?? null;
  } catch (error) {
    console.error('Unable to decode token', error);
    return null;
  }
}

const protectedPrefixes = ['/tenant', '/admin'];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  if (!protectedPrefixes.some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  const token = req.cookies.get(jwtCookieName)?.value;
  const role = resolveRole(token);

  if (!role) {
    const url = req.nextUrl.clone();
    url.pathname = '/login';
    return NextResponse.redirect(url);
  }

  if (pathname.startsWith('/tenant') && role !== 'tenant') {
    return NextResponse.redirect(new URL('/admin/dashboard', req.url));
  }

  if (pathname.startsWith('/admin') && role !== 'admin') {
    return NextResponse.redirect(new URL('/tenant/dashboard', req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/tenant/:path*', '/admin/:path*']
};
