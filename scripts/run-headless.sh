#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

usage() {
  cat <<'EOF'
Usage: scripts/run-headless.sh <job> [args...]

Jobs:
  ingest-semi [source-or-task...]
  daily-alert [args...]
  agent-report [args...]
  main-report [args...]
EOF
}

job="${1:-}"
if [[ -z "$job" ]]; then
  usage
  exit 1
fi
shift

export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

case "$job" in
  ingest-semi)
    prompt="/ingest-semi"
    if (($#)); then
      prompt="$prompt $*"
    fi

    exec claude -p \
      --bare \
      --add-dir "$repo_root" \
      --no-session-persistence \
      --permission-mode "${CLAUDE_PERMISSION_MODE:-bypassPermissions}" \
      --output-format text \
      "$prompt"
    ;;
  daily-alert)
    exec python3 agents/src/earnings_calendar.py "$@"
    ;;
  agent-report)
    exec python3 -m agents.src.report "$@"
    ;;
  main-report)
    exec python3 -m src.report "$@"
    ;;
  *)
    usage
    exit 1
    ;;
esac
