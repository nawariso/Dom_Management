'use client';

import { useState } from 'react';
import { initiatePayment } from '@/lib/api-client';

export function PaymentInitiation({ invoiceId, defaultAmount }: { invoiceId?: string; defaultAmount?: number }) {
  const [method, setMethod] = useState<'qr' | 'card'>('qr');
  const [amount, setAmount] = useState(defaultAmount ?? 0);
  const [message, setMessage] = useState('');
  const [qrCode, setQrCode] = useState('');

  const onSubmit = async () => {
    setMessage('Processing payment...');
    try {
      const payload = await initiatePayment({ method, amount, invoiceId });
      setQrCode(payload.qrCode ?? '');
      setMessage(payload.redirectUrl ? `Redirect to ${payload.redirectUrl}` : 'Payment initiated');
    } catch (error) {
      console.error(error);
      setMessage('Unable to start payment, please try again.');
    }
  };

  return (
    <div className="space-y-3 rounded-lg border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600">Payment method</p>
          <div className="mt-2 flex gap-2">
            <button
              className={`btn ${method === 'qr' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setMethod('qr')}
              type="button"
            >
              QR
            </button>
            <button
              className={`btn ${method === 'card' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setMethod('card')}
              type="button"
            >
              Card
            </button>
          </div>
        </div>
        <div>
          <label className="text-sm font-medium text-slate-600">Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(parseFloat(e.target.value))}
            className="ml-2 w-32 rounded-md border border-slate-300 px-3 py-2 text-right text-sm"
          />
        </div>
      </div>
      <button className="btn btn-primary" type="button" onClick={onSubmit}>
        Initiate {method === 'qr' ? 'QR' : 'card'} payment
      </button>
      {message && <p className="text-sm text-slate-600">{message}</p>}
      {qrCode && (
        <div className="rounded bg-slate-50 p-3 text-center text-xs font-mono text-slate-500">
          QR payload: {qrCode}
        </div>
      )}
    </div>
  );
}
