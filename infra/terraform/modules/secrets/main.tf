variable "namespace" {
  type        = string
  description = "Namespace to publish secrets"
}

variable "engine_path" {
  type        = string
  description = "Secret engine path"
}

variable "secrets" {
  type        = map(string)
  description = "Key/value secrets to publish"
}

resource "null_resource" "secrets" {
  triggers = merge(
    {
      namespace   = var.namespace
      engine_path = var.engine_path
    },
    var.secrets
  )
}

output "secret_keys" {
  value       = keys(var.secrets)
  description = "Keys stored in secret manager"
}
