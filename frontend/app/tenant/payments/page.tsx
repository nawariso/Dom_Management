'use client';

import { useEffect, useState } from 'react';
import { fetchPayments } from '@/lib/api-client';
import { PaymentInitiation } from '@/components/PaymentInitiation';

export default function TenantPaymentsPage() {
  const [payments, setPayments] = useState<{ id: string; amount: number; method: string; createdAt: string }[]>([]);

  useEffect(() => {
    fetchPayments('tenant').then(setPayments);
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Payments</h1>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Payment</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Amount</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Method</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Created</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {payments.map((payment) => (
              <tr key={payment.id}>
                <td className="px-4 py-2 font-mono text-slate-700">{payment.id}</td>
                <td className="px-4 py-2">${payment.amount.toFixed(2)}</td>
                <td className="px-4 py-2 capitalize">{payment.method}</td>
                <td className="px-4 py-2">{new Date(payment.createdAt).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <PaymentInitiation />
    </div>
  );
}
