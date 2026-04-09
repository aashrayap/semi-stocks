# Global Instructions

## Core Rules
- Treat this repo's wiki root as `wiki/` in the current checkout. Never write to `/Users/ash/Documents/2026/wiki` or `/Users/ash/Documents/2026/semi-stocks/wiki` from this workspace.
- For semi-stocks wiki ingest, query, or lint work, use the repo-local `ingest-semi` skill. In Claude invoke `/ingest-semi`; in Codex use the local `.codex/skills/ingest-semi/` skill.
- Read `wiki/schema.md` before any wiki mutation. After wiki writes, update `wiki/index.md`, rebuild the index, and append `wiki/log.md`.
- Route new evidence through `wiki/raw/` -> `wiki/sources/` -> `data/`. Do not write directly to `data/` from untracked source material.
- Run repo commands from the repo root. Working entrypoints: `python3 ~/.dot-agent/skills/wiki/scripts/rebuild_index.py wiki`, `python3 -m src.report`, `python3 agents/src/earnings_calendar.py --days 21`, `python3 -m agents.src.report --date YYYY-MM-DD`.

## Coding Conventions
- Prefer updating existing wiki pages and YAML files over creating near-duplicates.
- Keep tracked instructions and skills repo-relative so Conductor workspaces do not leak writes back to a source checkout.

## Workflow Expectations
- Install repo hooks in new clones or worktrees with `scripts/setup-hooks.sh`. The pre-commit hook blocks sensitive commits when the parent 2026 wiki or source semi-stocks checkout has stray edits.
- When the task touches earnings or 13F ingestion, read `data/research/earnings-pipeline.md` first and preserve semi-stocks-specific sections such as `Forward Claims`, `Thesis Signal`, and `Semi-stocks data`.
- Treat `agents/drafts/` and `agents/reports/` as sidecars. Promote reviewed facts into `wiki/` and `data/`; do not treat sidecar outputs as canonical truth.

## Conditional Guidance

### Planning
- Decide the landing layer first: raw evidence in `wiki/raw/`, synthesis in `wiki/sources/` or `wiki/concepts/`, structured state in `data/`, derived views in `src/` or `agents/`.

### Implementation
- If a request says "ingest", "query", or "lint" without a path, resolve candidates from `wiki/raw/` in this repo before looking anywhere else.
- For scheduled jobs, prefer deterministic Python entrypoints for reports and `scripts/run-headless.sh ingest-semi ...` when Claude needs to run non-interactively.

### Review
- Report drift, contract breaks, and missing verification first. If wiki or automation wiring changes, mention whether `scripts/check_repo_context.sh --force` and the relevant rebuild or report command were run.

## Anti-Patterns
- Hardcoding `/Users/ash/Documents/2026/...` paths in tracked repo files.
- Using the generic `/wiki` flow when the task is clearly about this repo's semi-stocks wiki.
- Editing `wiki/raw/` after ingest.
