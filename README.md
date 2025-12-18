# Dom Management Platform

A cloud-ready dormitory management platform that allows tenants to monitor water and electricity usage, pay bills (including subscription-based payments), and handle their own account lifecycle. The platform is designed to mimic the Thai Metropolitan Electricity Authority (MEA) experience while supporting automated CI/CD from development through production.

## System Overview
The platform provides an MEA-like experience for dorms: tenants self-serve meter visibility, invoices, and payments (including subscription renewals), while operators manage rooms, tariffs, and billing rules with auditable workflows. The system is intended to run across Dev → Staging → Production with observability, security, and automation built in from the start.

## Goals
- Provide self-service portals for tenants to view consumption, download invoices, and pay securely.
- Give dorm managers tools to configure rooms, tariffs, subscriptions, and payment rules.
- Deliver a cloud-native architecture with clear Dev → Staging → Production promotion flows and observability baked in.

## High-level Features
- **Tenant portal**: authentication, profile management, room association, usage dashboards, billing history, invoice downloads, subscription management, and payment confirmations.
- **Usage tracking**: water/electricity meter ingestion (manual entry, CSV upload, or device webhook), anomaly detection thresholds, monthly rollups, and cost calculation per tariff.
- **Billing & payments**: invoice generation, OTP-backed payments, Thai QR/credit card integrations (e.g., Omise/Stripe), subscription renewals, automatic receipts, and dunning flows for failed renewals.
- **Admin console**: room/tenant CRUD, tariff setup (peak/off-peak), subscription plan configuration, promotions, and role-based access (owner vs. staff).
- **Notifications**: email/SMS/LINE push for bill readiness, payment success/failure, and threshold alerts.
- **Audit & compliance**: activity logs, immutable payment records, and exportable reports.

## Architecture
## Architecture Overview
- **Frontend**: React or Next.js SPA/SSR with Tailwind for admin and tenant portals; integrates with payment widgets and LINE login if required.
- **Backend API**: Python FastAPI or Node.js NestJS service exposing REST/GraphQL for tenants/admins. Background jobs handled by Celery/Redis or BullMQ.
- **Data**: PostgreSQL for core data; Redis for caching/sessions; object storage (S3/GCS) for invoices and receipts.
- **Meter ingestion**: webhook endpoints for smart meters; manual entry UI; scheduled imports for CSV from legacy systems.
- **Billing engine**: periodic jobs to compute charges, generate PDF invoices, and queue payment intents via PSP.
- **Payments**: integrate PSP (Stripe/Omise) supporting Thai QR, cards, and subscription billing. Webhooks update invoice status and issue receipts.
- **Identity & RBAC**: JWT sessions with refresh tokens; RBAC enforcing tenant vs. admin vs. auditor roles; optional SSO for corporate dorms.
- **Observability**: OpenTelemetry traces, structured logs, metrics to Prometheus/Grafana, uptime checks, and alerting via Slack/LINE.

## Deployment
### Proposed Cloud Deployment
- **Kubernetes** (EKS/GKE/AKS) or managed PaaS; services containerized with Docker.
- **Ingress** via managed load balancer + HTTPS (ACM/Let’s Encrypt).
- **Databases**: managed PostgreSQL (RDS/Cloud SQL) with read replicas; Redis via ElastiCache/Memorystore; S3/GCS for files.
- **Secrets** in cloud secret manager; **CI/CD** injects via environment variables and sealed secrets.
- **File rendering**: invoice PDFs built in worker pods using headless Chromium.

## CI/CD Pipeline
- **Branch strategy**: `feature/*` → PR → `develop` (Dev environment) → tag release → `main` (Staging/Prod promotion via approvals).
- **Quality gates**: lint (ESLint/Prettier or Ruff/Black), unit/integration tests, type checks (TypeScript/MyPy), security scans (Snyk/Trivy), and IaC validation (Terraform fmt/validate/plan).
- **Build & deploy**:
  1. Build Docker images for frontend/backend, push to registry.
  2. Run database migrations (Alembic/Prisma) in release jobs.
  3. Deploy to Dev via Helmfile/Argo CD; run smoke tests.
  4. Promote to Staging with blue/green or canary; execute e2e tests (Playwright/Cypress).
  5. Manual approval → Production rollout with progressive delivery and automatic rollback on failed health checks.
- **Versioning & artifacts**: semver tags; attach Helm charts and migration bundles to releases.
- **Monitoring in pipeline**: publish coverage reports and lighthouse scores; notify Slack/LINE on pipeline status.

## Domain Model (initial)
- **Dorm**: id, name, address, contact info.
- **Building / Floor / Room**: hierarchical units with occupancy status and associated meters.
- **Tenant**: user profile, authentication identity, linked room(s), subscription plan, payment methods.
- **Meter**: type (water/electric), reading history, webhook credentials.
- **UsageRecord**: meter_id, period, consumption, cost breakdown.
- **Tariff**: pricing rules (fixed, tiered, time-of-use), taxes, fees.
- **Invoice**: tenant, period, line items (water/electric/base), status (pending/paid/overdue), PDF URL, PSP intent ids.
- **Payment**: transaction status, method, PSP reference, receipt URL.
- **Subscription**: plan, cycle, renewal date, dunning state.
- **AuditLog**: actor, action, entity, metadata, timestamp.

## Key User Flows
1. **Meter reading ingestion** → validate → compute charges → generate invoice → notify tenant.
2. **Tenant payment** → PSP checkout (QR/card) → webhook updates invoice → send receipt → update ledger.
3. **Subscription renewal** → pre-authorization → renewal attempt → retry schedule → suspend services and notify if unpaid.
4. **Admin operations** → manage rooms/tenants/tariffs → adjust invoices with approvals → export reports.

## Security & Compliance
- HTTPS everywhere; HSTS and CSRF protections on web.
- Token rotation, device-bound refresh tokens, optional MFA.
- PSP best practices: client-side tokenization, backend-only secret handling, idempotent webhooks.
- Data retention policies with PII minimization and encrypted storage (at rest + in transit).
- Backups with PITR for PostgreSQL; DR plan with multi-AZ and replicated storage.

## Suggested Technology Stack
- **Frontend**: Next.js + TypeScript, Tailwind, Playwright for e2e.
- **Backend**: FastAPI + SQLAlchemy + Alembic or NestJS + Prisma.
- **Workers**: Celery/RQ or BullMQ for billing cycles and webhooks.
- **Infra/IaC**: Terraform + Helmfile/Argo CD; GitHub Actions/GitLab CI for pipelines.
- **Payments**: Stripe/Omise with Thai QR support; supports subscriptions.
- **Notifications**: AWS SES/SNS or Twilio; LINE Messaging API optional.

## Roadmap (MVP → Production)
1. Implement tenant and admin auth, room assignment, and basic tariff-based billing.
2. Add meter ingestion + manual entry, invoice generation, and PSP payment flows.
3. Deliver subscription plans with automatic renewals and dunning.
4. Harden with observability, RBAC, audit logging, and DR strategy.
5. Package Helm charts, finalize CI/CD gates, and launch multi-tenant onboarding for general dorms.

## Local Smoke Test
Use the provided Makefile target to run a lightweight documentation smoke test that validates required sections exist in the
architecture guides. This helps ensure the end-to-end flow documentation remains consistent while the codebase is being
implemented.

```
make test
```

This document will evolve as the implementation starts; see `docs/system-architecture.md` for deeper diagrams and rollout details (to be expanded).
