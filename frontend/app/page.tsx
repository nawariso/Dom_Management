import Link from 'next/link';

export default function Home() {
  return (
    <main className="mx-auto max-w-5xl p-8">
      <div className="rounded-2xl bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-brand-800">Dom Management Portal</h1>
        <p className="mt-4 text-slate-600">
          Access tenant and administrator tools for smart meter tracking, billing, and payments.
        </p>
        <div className="mt-8 flex gap-4">
          <Link href="/login" className="btn btn-primary">
            Sign In
          </Link>
          <Link href="/tenant/dashboard" className="btn btn-secondary">
            Tenant Dashboard
          </Link>
          <Link href="/admin/dashboard" className="btn btn-secondary">
            Admin Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}
