'use client';

import { useState } from 'react';

export default function AdminSubscriptionPage() {
  const [autoBilling, setAutoBilling] = useState(true);
  const [message, setMessage] = useState('');

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Subscription controls</h1>
      <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
        <p className="text-sm text-slate-600">Toggle tenant-wide billing and renewal behaviors.</p>
        <label className="flex items-center gap-3 text-sm font-medium text-slate-800">
          <input
            type="checkbox"
            checked={autoBilling}
            onChange={(e) => {
              setAutoBilling(e.target.checked);
              setMessage('Saved changes');
            }}
            className="h-4 w-4 rounded border-slate-300"
          />
          Enable auto-billing for all tenants
        </label>
        <button className="btn btn-primary" type="button" onClick={() => setMessage('Tenant settings synchronized')}>
          Sync settings with backend
        </button>
        {message && <p className="text-sm text-slate-600">{message}</p>}
      </div>
    </div>
  );
}
