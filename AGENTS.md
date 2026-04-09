# Global Instructions

semi-stocks tracks AI infrastructure bottleneck rotation. Start each session at `TODO.md` and treat `README.md` as the landing page.

## Core Rules
- Treat this checkout's `wiki/` as the only writable semi-stocks wiki root. Do not write to `/Users/ash/Documents/2026/wiki` or `/Users/ash/Documents/2026/semi-stocks/wiki` from this workspace.
- For semi-stocks wiki ingest, query, or lint work, use the repo-local `ingest-semi` skill. In Claude invoke `/ingest-semi`; in Codex use `.codex/skills/ingest-semi/`.
- Canonical truth path: `wiki/raw/` -> `wiki/sources/` or `wiki/concepts/` -> `data/companies/` or `data/sources/` -> `data/thesis.yaml` -> reports.
- `data/` is the final authority when prose and structure disagree.
- Outputs under `agents/` are proposals until human review promotes them.

## Coding Conventions
- Keep tracked instructions, skills, and automation repo-relative so Conductor workspaces do not leak writes back to a source checkout.
- Prefer updating existing wiki pages and YAML files over creating near-duplicates.

## Workflow Expectations
- Install repo hooks in new clones or worktrees with `scripts/setup-hooks.sh`. The pre-commit hook blocks sensitive commits when the parent 2026 wiki or source semi-stocks checkout has stray edits.
- Run repo commands from the repo root. Working entrypoints: `python3 ~/.dot-agent/skills/wiki/scripts/rebuild_index.py wiki`, `python3 -m src.report`, `python3 agents/src/earnings_calendar.py --days 21`, `python3 -m agents.src.report --date YYYY-MM-DD`.
- Treat `agents/drafts/` and `agents/reports/` as sidecars. Promote reviewed facts into `wiki/` and `data/`; do not treat sidecar outputs as canonical truth.

## Conditional Guidance

### Orientation
- Read in order: `TODO.md`, `data/thesis.yaml`, `wiki/concepts/bottleneck-cascade.md`, `wiki/concepts/source-triangulation.md`, and `data/research/earnings-pipeline.md`.

### Canonical Research
- Put new raw evidence in `wiki/raw/`.
- Put event writeups in `wiki/sources/` and cross-cutting synthesis in `wiki/concepts/`.
- Promote durable facts to `data/companies/` or `data/sources/`.
- Update `data/thesis.yaml` only when structured evidence changes stage status, dates, or ticker mapping.

### Earnings
- Follow `data/research/earnings-pipeline.md`.
- Score prior `forward_claims` before ingesting a new quarter.
- Deep-dive names: CRWV, NVDA, MU, COHR, INTC, TSM, LITE.

### 13F
- Cross-check with SEC EDGAR and at least two aggregators before promotion.
- Treat Leopold/Baker divergence as a research signal to explain, not something to smooth over.

### Wiki Edits
- Read `wiki/schema.md` first.
- If a request says "ingest", "query", or "lint" without a path, resolve candidates from `wiki/raw/` in this repo before looking anywhere else.
- After wiki writes, update `wiki/index.md`, rebuild the index, and append `wiki/log.md`.

### Automation
- For scheduled jobs, prefer deterministic Python entrypoints for reports and `scripts/run-headless.sh ingest-semi ...` when Claude needs to run non-interactively.
- If wiki or automation wiring changes, mention whether `scripts/check_repo_context.sh --force` and the relevant rebuild or report command were run.

### Agent Lane
- Read `agents/CLAUDE.md` before working in `agents/`.
- Agents may read the full repo but may write only under `agents/`.

## Anti-Patterns
- Hardcoding `/Users/ash/Documents/2026/...` paths in tracked repo files.
- Using the generic `/wiki` flow when the task is clearly about this repo's semi-stocks wiki.
- Changing thesis state directly from raw notes or agent output.
- Storing canonical facts only in prose when they belong in `data/`.
- Editing `wiki/raw/` after ingest.
