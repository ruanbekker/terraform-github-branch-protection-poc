output "repository_full_name" {
  description = "Full name of the provisioned repository."
  value       = github_repository.poc.full_name
}

output "repository_html_url" {
  description = "Web URL of the provisioned repository."
  value       = github_repository.poc.html_url
}

output "clone_url" {
  description = "HTTPS clone URL of the provisioned repository."
  value       = github_repository.poc.http_clone_url
}

output "branch_protection_enabled" {
  description = "Whether the branch protection rule is applied."
  value       = var.enable_branch_protection
}

output "required_status_checks" {
  description = "Status check contexts required before merge."
  value       = local.required_status_checks
}
