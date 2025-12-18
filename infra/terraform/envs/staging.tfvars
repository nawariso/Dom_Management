environment = "staging"
environment_overrides = {
  namespace             = "staging"
  ingress_host          = "staging.dom-management.local"
  database_size         = "db.m5.large"
  database_storage_gb   = 200
  redis_plan            = "cache.m6g.large"
  bucket_tier           = "standard"
  tls_issuer            = "letsencrypt-staging"
  backup_retention_days = 14
}
