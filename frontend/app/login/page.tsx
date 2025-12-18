'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { login } from '@/lib/api-client';
import { parseToken } from '@/lib/auth';
import { getAccessToken } from '@/lib/tokenStorage';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login({ email, password });
      const token = getAccessToken();
      const parsed = parseToken(token);
      if (parsed?.role === 'admin') {
        router.push('/admin/dashboard');
      } else {
        router.push('/tenant/dashboard');
      }
    } catch (err) {
      console.error(err);
      setError('Unable to sign in, please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-lg items-center p-6">
      <form
        onSubmit={onSubmit}
        className="w-full space-y-4 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"
      >
        <h1 className="text-2xl font-bold text-brand-800">Welcome back</h1>
        <p className="text-sm text-slate-600">Sign in with your tenant or admin credentials.</p>
        <div className="space-y-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            placeholder="you@example.com"
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            placeholder="•••••••"
          />
        </div>
        {error && <p className="text-sm text-rose-600">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary w-full justify-center disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Signing in...' : 'Continue'}
        </button>
      </form>
    </main>
  );
}
