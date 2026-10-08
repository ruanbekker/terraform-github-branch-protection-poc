#!/usr/bin/env python3
"""Verify that every required status check context in Terraform maps to a
GitHub Actions job that actually reports it.

Branch protection only unblocks a PR once every context in
locals.required_status_checks reports success. GitHub reports the check name
as the job's `name:` if set, otherwise the job id. Renaming a job (or a
context) without updating the other side would leave PRs waiting forever for a
status that never arrives, so we fail fast here instead.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALS_TF = ROOT / "terraform" / "locals.tf"
WORKFLOWS_DIR = ROOT / ".github" / "workflows"


def required_contexts() -> list[str]:
    source = LOCALS_TF.read_text()
    match = re.search(
        r"required_status_checks\s*=\s*\[(.*?)\]", source, re.DOTALL
    )
    if not match:
        sys.exit(f"ERROR: required_status_checks not found in {LOCALS_TF}")
    return re.findall(r'"([^"]+)"', match.group(1))


def job_contexts(path: Path) -> list[str]:
    contexts: list[str] = []
    job_id: str | None = None
    pending_name: dict[str, bool] = {}
    in_jobs = False

    for line in path.read_text().splitlines():
        if re.match(r"^jobs:", line):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            in_jobs = False
            continue

        job_match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if job_match:
            job_id = job_match.group(1)
            pending_name[job_id] = True
            contexts.append(job_id)
            continue

        name_match = re.match(r"^    name:\s*(.+?)\s*$", line)
        if name_match and job_id and pending_name.get(job_id):
            name = name_match.group(1).strip("'\"")
            contexts[-1] = name
            pending_name[job_id] = False

    return contexts


def main() -> None:
    required = required_contexts()
    if not required:
        sys.exit(
            f"ERROR: no required status checks configured in {LOCALS_TF}"
        )

    workflow_files = sorted(WORKFLOWS_DIR.glob("*.yml")) + sorted(
        WORKFLOWS_DIR.glob("*.yaml")
    )
    if not workflow_files:
        sys.exit(f"ERROR: no workflow files found in {WORKFLOWS_DIR}")

    available: dict[str, str] = {}
    for path in workflow_files:
        for context in job_contexts(path):
            available.setdefault(context, path.name)

    missing = [c for c in required if c not in available]
    if missing:
        known = "\n".join(f"  - {c} ({f})" for c, f in sorted(available.items()))
        sys.exit(
            "ERROR: required status checks with no reporting job:\n"
            + "\n".join(f"  - {c}" for c in missing)
            + f"\nJobs found:\n{known}"
        )

    print("Required status checks and the jobs that report them:")
    for context in required:
        print(f"  - {context}  <-  {available[context]}")

    pulls_pr = False
    for path in workflow_files:
        text = path.read_text()
        if re.search(r"^\s+pull_request\s*:", text, re.MULTILINE) or re.search(
            r"^on:\s*\n\s+pull_request\s*$", text, re.MULTILINE
        ):
            pulls_pr = True
    if not pulls_pr:
        sys.exit(
            "ERROR: no workflow triggers on `pull_request`, so checks will "
            "never be reported on PRs."
        )
    print("OK: a workflow triggers on pull_request events.")


if __name__ == "__main__":
    main()
