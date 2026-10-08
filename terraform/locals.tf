locals {
  # Status check contexts that must report success before a PR can merge.
  # Each entry must match a GitHub Actions job id (or job name) reported by
  # .github/workflows/*.yml. scripts/check_status_contexts.py enforces this.
  required_status_checks = [
    "build",
    "test",
  ]
}
