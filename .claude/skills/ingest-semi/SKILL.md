---
name: ingest-semi
description: "Ingest, query, or lint the semi-stocks wiki in the current repo without falling back to the parent 2026 wiki."
argument-hint: "[source-or-task]"
disable-model-invocation: true
---

Use this skill when the task should operate on the semi-stocks wiki in the current checkout and must not touch `/Users/ash/Documents/2026/wiki` or another semi-stocks checkout.

## Fixed targets

- Wiki root: `wiki`
- Schema: `wiki/schema.md`
- Raw sources: `wiki/raw`
- Rebuild command: `python3 ~/.dot-agent/skills/wiki/scripts/rebuild_index.py wiki`

## Workflow

1. Read `wiki/schema.md` before doing anything else.
2. Treat `wiki/` in the current repo as the only wiki root for this skill. Do not use generic wiki discovery and do not write to `/Users/ash/Documents/2026/wiki`.
3. If `$ARGUMENTS` is empty, inspect `wiki/raw` for recently modified sources and suggest the best candidates.
4. If `$ARGUMENTS` names a file or folder without an absolute path, resolve it relative to `wiki/raw` first.
5. Follow the ingest, query, or lint workflow from `wiki/schema.md` rather than the generic wiki defaults when they differ.

## Ingest rules

- Never modify anything under `raw/`.
- Prefer updating existing pages in `sources/` and `concepts/` over creating duplicates.
- Keep tracked repo paths repo-relative so the skill works inside worktrees and Conductor workspaces.
- Preserve semi-stocks-specific sections such as `## Forward Claims`, `## Thesis Signal`, and `## Semi-stocks data` when they apply.
- When a source changes the thesis, bottleneck state, or tracked company signals, propose the corresponding `data/` patch explicitly.

## After every write

1. Update `wiki/index.md`.
2. Run `python3 ~/.dot-agent/skills/wiki/scripts/rebuild_index.py wiki`.
3. Append the operation to `wiki/log.md`.

ARGUMENTS: $ARGUMENTS
