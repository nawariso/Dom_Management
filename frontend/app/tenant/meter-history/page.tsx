'use client';

import { useEffect, useState } from 'react';
import { fetchMeterHistory } from '@/lib/api-client';
import { MeterEntryForm } from '@/components/MeterEntryForm';

export default function TenantMeterHistoryPage() {
  const [history, setHistory] = useState<{ timestamp: string; value: number }[]>([]);

  useEffect(() => {
    fetchMeterHistory('tenant').then(setHistory);
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Meter history</h1>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Captured</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">kWh</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {history.map((row) => (
              <tr key={row.timestamp}>
                <td className="px-4 py-2">{new Date(row.timestamp).toLocaleString()}</td>
                <td className="px-4 py-2">{row.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <MeterEntryForm />
    </div>
  );
}
