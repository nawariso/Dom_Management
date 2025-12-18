environment = "dev"
environment_overrides = {
  namespace             = "dev"
  ingress_host          = "dev.dom-management.local"
  database_size         = "db.t3.small"
  database_storage_gb   = 40
  redis_plan            = "cache.t3.micro"
  bucket_tier           = "standard"
  tls_issuer            = "letsencrypt-staging"
  backup_retention_days = 7
}
