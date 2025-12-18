'use client';

import { useState } from 'react';
import { downloadInvoice } from '@/lib/api-client';

export function InvoiceDownload({ invoiceId }: { invoiceId: string }) {
  const [status, setStatus] = useState('');

  const handleDownload = async () => {
    setStatus('Preparing download...');
    try {
      const blob = await downloadInvoice(invoiceId);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${invoiceId}.pdf`;
      link.click();
      URL.revokeObjectURL(url);
      setStatus('Invoice downloaded');
    } catch (error) {
      console.error(error);
      setStatus('Unable to download invoice');
    }
  };

  return (
    <button onClick={handleDownload} className="btn btn-secondary" type="button">
      Download
      {status && <span className="ml-2 text-xs text-slate-500">{status}</span>}
    </button>
  );
}
