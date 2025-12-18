export const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:4000/api';
export const websocketUrl = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:4000/socket';
export const jwtCookieName = process.env.JWT_COOKIE_NAME || 'dm_access_token';
export const refreshCookieName = process.env.REFRESH_COOKIE_NAME || 'dm_refresh_token';
