'use client';

import Cookies from 'js-cookie';
import { jwtCookieName, refreshCookieName } from './config';

export function getAccessToken() {
  return Cookies.get(jwtCookieName);
}

export function getRefreshToken() {
  return Cookies.get(refreshCookieName);
}

export function setTokens(accessToken: string, refreshToken?: string) {
  Cookies.set(jwtCookieName, accessToken, { sameSite: 'lax' });
  if (refreshToken) {
    Cookies.set(refreshCookieName, refreshToken, { sameSite: 'lax' });
  }
}

export function clearTokens() {
  Cookies.remove(jwtCookieName);
  Cookies.remove(refreshCookieName);
}
