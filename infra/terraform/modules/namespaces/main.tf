variable "namespaces" {
  type        = list(string)
  description = "Namespaces to ensure exist"
}

resource "null_resource" "namespaces" {
  count = length(var.namespaces)

  triggers = {
    namespace = element(var.namespaces, count.index)
  }
}

output "namespaces" {
  value       = var.namespaces
  description = "List of namespaces provisioned"
}
