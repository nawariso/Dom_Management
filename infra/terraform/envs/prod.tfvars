environment = "prod"

environment_overrides = {
  ingress_host        = "app.example.com"
  tls_issuer          = "letsencrypt-prod"
  database_storage_gb = 500
  replicas            = 3
  bucket_tier         = "infrequent-access"
}
