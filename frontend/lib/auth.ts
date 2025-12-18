import { decodeJwt } from 'jose';

type DecodedToken = {
  sub?: string;
  role?: 'tenant' | 'admin';
  exp?: number;
};

export function parseToken(token: string | undefined): DecodedToken | null {
  if (!token) return null;
  try {
    return decodeJwt(token) as DecodedToken;
  } catch (error) {
    console.error('Unable to decode token', error);
    return null;
  }
}
