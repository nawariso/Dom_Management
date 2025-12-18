'use client';

import { useEffect, useState } from 'react';
import { fetchThresholds, updateThreshold } from '@/lib/api-client';
import type { Role } from '@/lib/api-client';

export function ThresholdAlert({ role }: { role: Role }) {
  const [thresholds, setThresholds] = useState<{ metric: string; threshold: number; breached: boolean }[]>([]);
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    fetchThresholds(role).then(setThresholds);
  }, [role]);

  const handleUpdate = async (metric: string, value: number) => {
    setSaving(true);
    setFeedback('Saving threshold...');
    try {
      await updateThreshold(metric, value);
      setThresholds((prev) => prev.map((t) => (t.metric === metric ? { ...t, threshold: value } : t)));
      setFeedback('Threshold updated');
    } catch (error) {
      console.error(error);
      setFeedback('Unable to update threshold');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
      <h3 className="text-lg font-semibold text-brand-800">Threshold alerts</h3>
      <p className="text-sm text-slate-600">Control notifications for usage and billing anomalies.</p>
      <div className="space-y-2">
        {thresholds.map((item) => (
          <div
            key={item.metric}
            className="flex items-center justify-between rounded-md border border-slate-100 bg-slate-50 px-3 py-2"
          >
            <div>
              <p className="font-medium capitalize text-slate-800">{item.metric}</p>
              <p className="text-xs text-slate-500">Current: {item.threshold}</p>
              {item.breached && <span className="text-xs font-semibold text-amber-600">Alert triggered</span>}
            </div>
            <div className="flex items-center gap-2">
              <input
                type="number"
                className="w-24 rounded border border-slate-300 px-2 py-1 text-sm"
                defaultValue={item.threshold}
                onBlur={(e) => handleUpdate(item.metric, Number(e.target.value))}
              />
              <span className="text-xs text-slate-500">units</span>
            </div>
          </div>
        ))}
      </div>
      {feedback && <p className="text-sm text-slate-600">{feedback}</p>}
      {saving && <p className="text-xs text-slate-500">Updating...</p>}
    </div>
  );
}
