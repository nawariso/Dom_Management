'use client';

import { useEffect, useState } from 'react';
import { fetchDashboard } from '@/lib/api-client';

export default function TenantSubscriptionPage() {
  const [plan, setPlan] = useState('Standard');
  const [status, setStatus] = useState('active');
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    fetchDashboard('tenant').then((data) => {
      setBalance(data.metrics.outstandingBalance ?? 0);
    });
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Subscription</h1>
      <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
        <p className="text-sm text-slate-600">Manage your subscription and auto-reload settings.</p>
        <div className="flex flex-wrap items-center gap-4 text-sm">
          <span className="rounded-full bg-brand-50 px-3 py-1 font-medium text-brand-800">Plan: {plan}</span>
          <span className="rounded-full bg-emerald-50 px-3 py-1 font-medium text-emerald-700 capitalize">{status}</span>
          <span className="rounded-full bg-amber-50 px-3 py-1 font-medium text-amber-700">
            Outstanding balance: ${balance.toFixed(2)}
          </span>
        </div>
        <button className="btn btn-primary" type="button" onClick={() => setPlan('Premium')}>
          Upgrade to Premium
        </button>
      </div>
    </div>
  );
}
