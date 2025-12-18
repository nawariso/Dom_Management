import { DashboardLayout } from '@/components/DashboardLayout';

export default function TenantLayout({ children }: { children: React.ReactNode }) {
  return <DashboardLayout role="tenant">{children}</DashboardLayout>;
}
