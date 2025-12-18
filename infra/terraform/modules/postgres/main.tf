variable "name" {
  type        = string
  description = "Database name"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace for secret distribution"
}

variable "instance_size" {
  type        = string
  description = "Instance class or tier"
}

variable "storage_gb" {
  type        = number
  description = "Allocated storage in GB"
}

variable "backup_retention_days" {
  type        = number
  description = "Retention days for backups"
}

variable "replicas" {
  type        = number
  description = "Number of replicas"
  default     = 1
}

resource "null_resource" "postgres" {
  triggers = {
    name                  = var.name
    namespace             = var.namespace
    instance_size         = var.instance_size
    storage_gb            = var.storage_gb
    backup_retention_days = var.backup_retention_days
    replicas              = var.replicas
  }
}

output "connection_uri" {
  description = "Example PostgreSQL connection URI"
  value       = "postgresql://${var.name}.${var.namespace}.svc.cluster.local:5432/${var.name}"
}

output "secret_name" {
  description = "Secret holding connection details"
  value       = "${var.name}-database-credentials"
}
