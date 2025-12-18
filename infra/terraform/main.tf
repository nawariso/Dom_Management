terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = ">= 3.2.1"
    }
  }
}

variable "environment" {
  description = "Deployment environment (dev|staging|prod)"
  type        = string
  default     = "dev"
}

variable "environment_overrides" {
  description = "Optional overrides for the selected environment map"
  type        = map(any)
  default     = {}
}

locals {
  env_config = {
    dev = {
      namespace              = "dev"
      database_size          = "db.t3.medium"
      database_storage_gb    = 50
      redis_plan             = "cache.t3.micro"
      replicas               = 1
      bucket_tier            = "standard"
      ingress_host           = "dev.app.example.com"
      tls_issuer             = "letsencrypt-staging"
      backup_retention_days  = 7
      secret_engine          = "dev"
    }
    staging = {
      namespace              = "staging"
      database_size          = "db.m5.large"
      database_storage_gb    = 200
      redis_plan             = "cache.m6g.large"
      replicas               = 2
      bucket_tier            = "standard"
      ingress_host           = "staging.app.example.com"
      tls_issuer             = "letsencrypt-staging"
      backup_retention_days  = 14
      secret_engine          = "staging"
    }
  }

  base     = lookup(local.env_config, var.environment, local.env_config.dev)
  selected = merge(local.base, var.environment_overrides)
}

module "namespaces" {
  source     = "./modules/namespaces"
  namespaces = [local.selected.namespace]
}

module "postgres" {
  source                = "./modules/postgres"
  name                  = "dom-management"
  namespace             = local.selected.namespace
  instance_size         = local.selected.database_size
  storage_gb            = local.selected.database_storage_gb
  backup_retention_days = local.selected.backup_retention_days
  replicas              = local.selected.replicas
}

module "redis" {
  source            = "./modules/redis"
  name              = "dom-management-cache"
  namespace         = local.selected.namespace
  plan              = local.selected.redis_plan
  high_availability = var.environment != "dev"
}

module "object_storage" {
  source      = "./modules/object_storage"
  bucket_name = "dom-management-${var.environment}"
  tier        = local.selected.bucket_tier
  versioning  = true
}

module "ingress" {
  source      = "./modules/ingress"
  name        = "dom-management"
  namespace   = local.selected.namespace
  host        = local.selected.ingress_host
  tls_issuer  = local.selected.tls_issuer
}

module "secrets" {
  source      = "./modules/secrets"
  namespace   = local.selected.namespace
  engine_path = local.selected.secret_engine
  secrets = {
    database_url = module.postgres.connection_uri
    redis_url    = module.redis.endpoint
    bucket_name  = module.object_storage.bucket_name
  }
}

output "namespace" {
  value = module.namespaces.namespaces
}

output "ingress_host" {
  value = module.ingress.host
}
