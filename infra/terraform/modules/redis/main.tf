variable "name" {
  type        = string
  description = "Redis deployment name"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace"
}

variable "plan" {
  type        = string
  description = "Redis plan or instance size"
}

variable "high_availability" {
  type        = bool
  description = "Enable HA settings"
  default     = false
}

resource "null_resource" "redis" {
  triggers = {
    name              = var.name
    namespace         = var.namespace
    plan              = var.plan
    high_availability = tostring(var.high_availability)
  }
}

output "endpoint" {
  value       = "redis://${var.name}.${var.namespace}.svc.cluster.local:6379"
  description = "Redis endpoint"
}
