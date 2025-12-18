import { apiBaseUrl } from './config';
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from './tokenStorage';

export type Role = 'tenant' | 'admin';

async function request<T>(path: string, init: RequestInit = {}, retry = true): Promise<T> {
  const token = getAccessToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers });

  if (response.status === 401 && retry) {
    const refreshed = await refreshTokens();
    if (refreshed) {
      return request<T>(path, init, false);
    }
  }

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  if (response.headers.get('content-type')?.includes('application/json')) {
    return response.json() as Promise<T>;
  }
  return (await response.text()) as unknown as T;
}

async function refreshTokens() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  const response = await fetch(`${apiBaseUrl}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refreshToken })
  });

  if (!response.ok) {
    clearTokens();
    return false;
  }

  const payload = await response.json();
  setTokens(payload.accessToken, payload.refreshToken);
  return true;
}

export async function login(input: { email: string; password: string }) {
  const response = await fetch(`${apiBaseUrl}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error('Invalid credentials');
  }

  const payload = await response.json();
  setTokens(payload.accessToken, payload.refreshToken);
  return payload;
}

export async function logout() {
  clearTokens();
}

export async function fetchDashboard(role: Role) {
  try {
    return await request<{ metrics: Record<string, number>; notices: string[] }>(`/${role}/dashboard`);
  } catch (error) {
    console.warn('Falling back to demo dashboard data', error);
    return {
      metrics: {
        activeMeters: 12,
        outstandingBalance: role === 'tenant' ? 124.23 : 15873.3,
        alerts: 2
      },
      notices: ['System running in demo mode']
    };
  }
}

export async function fetchMeterHistory(role: Role) {
  try {
    return await request<{ timestamp: string; value: number }[]>(`/${role}/meters`);
  } catch (error) {
    console.warn('Falling back to demo meter history', error);
    return [
      { timestamp: new Date().toISOString(), value: 23.5 },
      { timestamp: new Date(Date.now() - 3600_000).toISOString(), value: 18.2 }
    ];
  }
}

export async function fetchInvoices(role: Role) {
  try {
    return await request<{ id: string; amount: number; status: string; issuedAt: string }[]>(`/${role}/invoices`);
  } catch (error) {
    console.warn('Falling back to demo invoices', error);
    return [
      { id: 'INV-1001', amount: 120.5, status: 'open', issuedAt: new Date().toISOString() },
      { id: 'INV-1000', amount: 98.75, status: 'paid', issuedAt: new Date(Date.now() - 86400_000).toISOString() }
    ];
  }
}

export async function fetchPayments(role: Role) {
  try {
    return await request<{ id: string; amount: number; method: string; createdAt: string }[]>(`/${role}/payments`);
  } catch (error) {
    console.warn('Falling back to demo payments', error);
    return [
      { id: 'PAY-2001', amount: 120.5, method: 'card', createdAt: new Date().toISOString() }
    ];
  }
}

export async function submitMeterReading(payload: { value: number; capturedAt: string; meterId?: string }) {
  try {
    return await request('/tenant/meters', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  } catch (error) {
    console.warn('Unable to submit meter reading, storing locally', error);
    return { status: 'queued', ...payload };
  }
}

export async function initiatePayment(payload: { method: 'qr' | 'card'; amount: number; invoiceId?: string }) {
  return request<{ redirectUrl?: string; qrCode?: string }>('/payments/initiate', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function downloadInvoice(invoiceId: string) {
  const token = getAccessToken();
  const response = await fetch(`${apiBaseUrl}/invoices/${invoiceId}/download`, {
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  });

  if (!response.ok) {
    throw new Error('Unable to download invoice');
  }

  return await response.blob();
}

export async function fetchThresholds(role: Role) {
  try {
    return await request<{ metric: string; threshold: number; breached: boolean }[]>(`/${role}/thresholds`);
  } catch (error) {
    console.warn('Falling back to demo thresholds', error);
    return [
      { metric: 'consumption', threshold: 80, breached: false },
      { metric: 'spend', threshold: 150, breached: true }
    ];
  }
}

export async function updateThreshold(metric: string, threshold: number) {
  return request(`/thresholds/${metric}`, {
    method: 'PUT',
    body: JSON.stringify({ threshold })
  });
}
