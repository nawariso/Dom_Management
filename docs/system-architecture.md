# System Architecture

## 1. Environments & Promotion
- **Dev**: auto-deploy on merges to `develop`; seeds sample data; relaxed scaling; feature flags enabled.
- **Staging**: mirrors prod topology; used for release candidates and e2e; seeded with anonymized prod data; blue/green or canary enabled.
- **Production**: multi-AZ Kubernetes with HPA; WAF + rate limiting; monitored SLOs and alerting policies.
- Promotion requires: tests ≥90% pass, coverage reports, successful migrations in staging, manual approval for prod.

## 2. Service Topology
- **Gateway/Ingress**: Nginx/ALB ingress with path routing to frontend and API; cert-manager manages TLS.
- **Frontend**: Next.js app served via CDN; static assets cached; API calls through gateway.
- **API service**: FastAPI/NestJS running behind Horizontal Pod Autoscaler; uses Redis for caching and Celery/BullMQ for async jobs.
- **Worker**: processes billing cycles, PSP webhooks, invoice PDF rendering (headless Chromium), notifications, dunning retries.
- **Database**: PostgreSQL primary + read replica; Redis cluster for cache/session; object storage for documents.
- **Observability stack**: Prometheus, Grafana, Loki/ELK, Jaeger/Tempo, Alertmanager, Synthetics.

## 3. Data Flows
1. **Meter ingestion**: webhook/CSV/manual → API validates → queue job → compute usage → persist UsageRecord → trigger billing.
2. **Billing**: scheduler (CronJob) triggers monthly/weekly run → query usage → calculate tariffs → create Invoice → enqueue PDF render → notify tenant.
3. **Payments**: tenant initiates payment → PSP checkout → webhook with signature → worker updates Invoice/Payment, issues receipt, and logs audit.
4. **Subscription renewal**: nightly job finds renewals → creates payment intents → retries with exponential backoff → moves to dunning after N failures.

## 4. Security Controls
- JWT access + refresh tokens; rotate keys via JWKS; enforce RBAC at route and data layer.
- All secrets stored in cloud secret manager; injected via sealed secrets and environment variables.
- Database: row-level security for tenant isolation in multi-tenant mode; encryption at rest; TLS in transit.
- Webhooks: HMAC signature verification + idempotency keys; store replay protection tokens.
- Backups: daily snapshots + PITR; restore playbooks tested quarterly.

## 5. CI/CD Blueprint (GitHub Actions example)
- **Workflows**:
  - `lint-test.yml`: run lint, type checks, unit tests on PR; upload coverage and preview docs.
  - `build-image.yml`: build/push Docker images on `develop`/`main` using buildx + cache; scan with Trivy.
  - `deploy-dev.yml`: on `develop` success, deploy to Dev via Argo CD; run smoke tests.
  - `deploy-staging.yml`: on release tags, deploy to Staging; run migrations, e2e tests, and Lighthouse.
  - `deploy-prod.yml`: manual approval; progressive rollout with Argo Rollouts; post-deploy health checks.
  - `iac-validate.yml`: terraform fmt/validate/plan on infra changes.
- **Artifacts & releases**: Helm charts versioned per app; migrations bundled; changelog generated from PR labels.

## 6. Subscription & Billing Design
- **Plans**: monthly/annual with base fee + per-usage charges; discounts/promo codes; trial handling.
- **Billing model**: invoices contain subscription line + metered usage; proration when tenants move rooms mid-cycle.
- **Dunning**: retry schedule (e.g., 1h, 24h, 72h) with escalating notifications; auto-suspend after threshold; resume on payment.
- **Accounting**: immutable ledger entries per payment event; export to CSV; reconcile PSP payouts with invoices.

## 7. Operational Playbooks
- **Runbooks**: incident response for payment webhook failures, billing anomalies, and database contention.
- **Feature flags**: LaunchDarkly/ConfigCat or OSS equivalent; required for rollout of new payment methods.
- **Migrations**: zero-downtime strategy using online DDL, backward-compatible API changes, and dual writes when needed.
- **Testing pyramid**: unit → service → contract tests for PSP webhooks → e2e with synthetic meters.

## 8. Next Steps for Implementation
1. Scaffold Next.js frontend and FastAPI/NestJS backend with authentication and RBAC.
2. Define DB schema (SQLAlchemy/Prisma) for entities in README; set up migrations.
3. Implement meter ingestion endpoints + admin UI for manual entry.
4. Build billing engine, invoice PDFs, and PSP integration with webhooks and dunning.
5. Package Helm charts and Terraform modules for core infra; wire GitHub Actions workflows.
6. Add observability defaults (OTEL exporters, dashboards, alerts) and security baselines.
