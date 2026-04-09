#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$repo_root" config core.hooksPath .githooks
chmod +x "$repo_root/.githooks/pre-commit"
chmod +x "$repo_root/scripts/check_repo_context.sh"
chmod +x "$repo_root/scripts/run-headless.sh"

printf 'Installed repo-local hooks at %s/.githooks\n' "$repo_root"
