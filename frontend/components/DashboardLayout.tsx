'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';
import clsx from 'clsx';

const tenantLinks = [
  { href: '/tenant/dashboard', label: 'Dashboard' },
  { href: '/tenant/meter-history', label: 'Meter history' },
  { href: '/tenant/invoices', label: 'Invoices' },
  { href: '/tenant/payments', label: 'Payments' },
  { href: '/tenant/subscription', label: 'Subscription' }
];

const adminLinks = [
  { href: '/admin/dashboard', label: 'Dashboard' },
  { href: '/admin/meter-history', label: 'Meter history' },
  { href: '/admin/invoices', label: 'Invoices' },
  { href: '/admin/payments', label: 'Payments' },
  { href: '/admin/subscription', label: 'Subscription' }
];

export function DashboardLayout({
  role,
  children
}: {
  role: 'tenant' | 'admin';
  children: ReactNode;
}) {
  const pathname = usePathname();
  const links = role === 'admin' ? adminLinks : tenantLinks;

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 border-r border-slate-200 bg-white">
        <div className="px-6 py-4">
          <p className="text-xs font-semibold uppercase text-slate-500">{role} area</p>
          <h1 className="text-xl font-bold text-brand-800">Dom Manager</h1>
        </div>
        <nav className="mt-4 space-y-1 px-2">
          {links.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                pathname === href ? 'bg-brand-50 text-brand-800 ring-1 ring-brand-200' : 'text-slate-700 hover:bg-slate-50'
              )}
            >
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 bg-slate-50 p-6">
        <div className="mx-auto max-w-5xl space-y-4">{children}</div>
      </main>
    </div>
  );
}
