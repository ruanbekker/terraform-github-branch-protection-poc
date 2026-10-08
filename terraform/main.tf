resource "github_repository" "poc" {
  name        = var.repository_name
  description = "POC: branch protection with required build/test status checks"
  visibility  = var.repository_visibility

  auto_init              = false
  has_issues             = true
  has_wiki               = false
  has_discussions        = false
  allow_merge_commit     = false
  allow_squash_merge     = true
  allow_rebase_merge     = false
  delete_branch_on_merge = true
}

resource "github_branch_protection" "main" {
  count = var.enable_branch_protection ? 1 : 0

  repository_id  = github_repository.poc.node_id
  pattern        = var.protected_branch
  enforce_admins = true

  required_status_checks {
    strict   = var.strict_status_checks
    contexts = local.required_status_checks
  }

  required_pull_request_reviews {
    required_approving_review_count = var.required_approving_review_count
    dismiss_stale_reviews           = true
  }

  require_conversation_resolution = true
  allows_deletions                = false
  allows_force_pushes             = false
}
