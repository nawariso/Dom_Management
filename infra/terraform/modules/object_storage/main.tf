variable "bucket_name" {
  type        = string
  description = "Bucket name"
}

variable "tier" {
  type        = string
  description = "Storage tier"
}

variable "versioning" {
  type        = bool
  description = "Enable versioning"
  default     = true
}

resource "null_resource" "bucket" {
  triggers = {
    bucket_name = var.bucket_name
    tier        = var.tier
    versioning  = tostring(var.versioning)
  }
}

output "bucket_name" {
  value       = var.bucket_name
  description = "Created bucket name"
}
