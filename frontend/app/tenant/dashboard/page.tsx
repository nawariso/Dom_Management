'use client';

import { useEffect, useState } from 'react';
import { fetchDashboard } from '@/lib/api-client';
import { ThresholdAlert } from '@/components/ThresholdAlert';

export default function TenantDashboardPage() {
  const [metrics, setMetrics] = useState<Record<string, number>>({});
  const [notices, setNotices] = useState<string[]>([]);

  useEffect(() => {
    fetchDashboard('tenant').then((data) => {
      setMetrics(data.metrics);
      setNotices(data.notices);
    });
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Tenant dashboard</h1>
      <div className="grid gap-4 sm:grid-cols-3">
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key} className="rounded-lg border border-slate-200 bg-white p-4">
            <p className="text-sm capitalize text-slate-500">{key}</p>
            <p className="text-2xl font-semibold text-brand-800">{value}</p>
          </div>
        ))}
      </div>
      {notices.length > 0 && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-amber-800">
          <h2 className="font-semibold">Notices</h2>
          <ul className="list-disc pl-4 text-sm">
            {notices.map((notice) => (
              <li key={notice}>{notice}</li>
            ))}
          </ul>
        </div>
      )}
      <ThresholdAlert role="tenant" />
    </div>
  );
}
