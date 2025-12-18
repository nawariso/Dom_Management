'use client';

import { useState } from 'react';
import { submitMeterReading } from '@/lib/api-client';

export function MeterEntryForm() {
  const [value, setValue] = useState('');
  const [message, setMessage] = useState('');

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const numericValue = parseFloat(value);
    if (Number.isNaN(numericValue)) {
      setMessage('Please enter a valid number');
      return;
    }
    setMessage('Sending reading...');
    const response = await submitMeterReading({
      value: numericValue,
      capturedAt: new Date().toISOString()
    });
    setMessage(`Meter reading saved (${JSON.stringify(response)})`);
    setValue('');
  };

  return (
    <form onSubmit={onSubmit} className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
      <div>
        <label className="text-sm font-semibold text-slate-700">Manual meter entry</label>
        <input
          type="number"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="kWh"
          className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          required
        />
      </div>
      <button className="btn btn-primary" type="submit">
        Save reading
      </button>
      {message && <p className="text-sm text-slate-600">{message}</p>}
    </form>
  );
}
