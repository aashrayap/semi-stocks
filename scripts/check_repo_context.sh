#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [[ "${SEMI_CONTEXT_ALLOW_EXTERNAL_CHANGES:-0}" == "1" ]]; then
  exit 0
fi

staged_files="$(git diff --cached --name-only)"
needs_check=0

while IFS= read -r path; do
  case "$path" in
    wiki/*|data/*|.codex/*|.claude/*|AGENTS.md|CLAUDE.md)
      needs_check=1
      break
      ;;
  esac
done <<< "$staged_files"

if [[ "${1:-}" != "--force" && $needs_check -eq 0 ]]; then
  exit 0
fi

workspace_wiki="$repo_root/wiki"
external_targets=(
  "/Users/ash/Documents/2026/wiki"
  "/Users/ash/Documents/2026/semi-stocks/wiki"
)

dirty_targets=()

for target in "${external_targets[@]}"; do
  [[ -e "$target" ]] || continue

  owner_root="$(git -C "$(dirname "$target")" rev-parse --show-toplevel 2>/dev/null || true)"
  [[ -n "$owner_root" ]] || continue

  rel_target="${target#$owner_root/}"
  status="$(git -C "$owner_root" status --short -- "$rel_target" 2>/dev/null || true)"
  [[ -n "$status" ]] || continue

  dirty_targets+=("$target"$'\n'"$status")
done

if ((${#dirty_targets[@]} == 0)); then
  exit 0
fi

cat <<EOF
repo-context check failed

This workspace should write to:
  $workspace_wiki

Dirty external wiki targets were detected:
EOF

for item in "${dirty_targets[@]}"; do
  printf '\n%s\n' "$item"
done

cat <<'EOF'

If those edits are intentional, re-run with:
  SEMI_CONTEXT_ALLOW_EXTERNAL_CHANGES=1 git commit ...

Otherwise move the changes into this workspace or clean the external repo before committing here.
EOF

exit 1
