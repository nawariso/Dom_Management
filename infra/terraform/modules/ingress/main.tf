variable "name" {
  type        = string
  description = "Ingress or gateway name"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace"
}

variable "host" {
  type        = string
  description = "Public hostname"
}

variable "tls_issuer" {
  type        = string
  description = "ClusterIssuer or Issuer for TLS"
}

resource "null_resource" "ingress" {
  triggers = {
    name       = var.name
    namespace  = var.namespace
    host       = var.host
    tls_issuer = var.tls_issuer
  }
}

output "host" {
  value       = var.host
  description = "Hostname exposed"
}
