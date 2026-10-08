variable "github_owner" {
  description = "GitHub user or organization that owns the repository. Falls back to GITHUB_OWNER when null."
  type        = string
  default     = null
}

variable "github_token" {
  description = "GitHub token with repo administration permissions. Falls back to GITHUB_TOKEN when null."
  type        = string
  default     = null
  sensitive   = true
}

variable "repository_name" {
  description = "Name of the demo repository."
  type        = string
  default     = "terraform-github-branch-protection-poc"
}

variable "repository_visibility" {
  description = "Visibility of the demo repository."
  type        = string
  default     = "public"

  validation {
    condition     = contains(["public", "private", "internal"], var.repository_visibility)
    error_message = "repository_visibility must be public, private or internal."
  }
}

variable "protected_branch" {
  description = "Branch pattern protected by the branch protection rule."
  type        = string
  default     = "main"
}

variable "enable_branch_protection" {
  description = "Toggle the branch protection rule. Set to false for the initial bootstrap push, then apply again with true."
  type        = bool
  default     = true
}

variable "strict_status_checks" {
  description = "Require the branch to be up to date with the base branch before the required status checks can pass."
  type        = bool
  default     = true
}

variable "required_approving_review_count" {
  description = "Number of approving reviews required before merging (0-6). Kept at 0 so the status checks are the merge gate in this POC."
  type        = number
  default     = 0

  validation {
    condition     = var.required_approving_review_count >= 0 && var.required_approving_review_count <= 6
    error_message = "required_approving_review_count must be between 0 and 6."
  }
}
