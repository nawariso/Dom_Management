'use client';

import { useEffect, useState } from 'react';
import { fetchInvoices } from '@/lib/api-client';
import { InvoiceDownload } from '@/components/InvoiceDownload';
import { PaymentInitiation } from '@/components/PaymentInitiation';

export default function TenantInvoicesPage() {
  const [invoices, setInvoices] = useState<{
    id: string;
    amount: number;
    status: string;
    issuedAt: string;
  }[]>([]);

  useEffect(() => {
    fetchInvoices('tenant').then(setInvoices);
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-800">Invoices</h1>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Invoice</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Amount</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Issued</th>
              <th className="px-4 py-2 text-left font-semibold text-slate-600">Status</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {invoices.map((invoice) => (
              <tr key={invoice.id}>
                <td className="px-4 py-2 font-mono text-slate-700">{invoice.id}</td>
                <td className="px-4 py-2">${invoice.amount.toFixed(2)}</td>
                <td className="px-4 py-2">{new Date(invoice.issuedAt).toLocaleDateString()}</td>
                <td className="px-4 py-2 capitalize">{invoice.status}</td>
                <td className="px-4 py-2 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <InvoiceDownload invoiceId={invoice.id} />
                    {invoice.status !== 'paid' && (
                      <PaymentInitiation invoiceId={invoice.id} defaultAmount={invoice.amount} />
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
