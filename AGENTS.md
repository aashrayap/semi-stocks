# semi-stocks

Research repo tracking AI infrastructure bottleneck rotation. Start each session at `TODO.md`. Treat `README.md` as the landing page and use the docs below for canonical detail.

## Core Rules

- Read current thesis state from `data/thesis.yaml`, not copied prose.
- Canonical truth path: `wiki/raw/` -> `wiki/sources/` or `wiki/concepts/` -> `data/companies/` or `data/sources/` -> `data/thesis.yaml` -> reports.
- `data/` is the final authority when prose and structure disagree.
- Do not create a new hand-maintained truth lane.
- Outputs under `agents/` are proposals until human review promotes them.

## Repo Map

- `TODO.md` - current priorities
- `data/thesis.yaml` - bottleneck control plane, next earnings dates, ticker map
- `data/research/earnings-pipeline.md` - canonical ingest and promotion path
- `data/research/13f-pipeline-design.md` - 13F automation direction
- `wiki/schema.md` - wiki rules and bookkeeping
- `wiki/concepts/bottleneck-cascade.md` - thesis overview
- `wiki/concepts/source-triangulation.md` - how SemiAnalysis, Leopold, and Baker fit together
- `agents/` - sidecar lane with its own boundary rules

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
- Update `wiki/index.md` and `wiki/log.md` when adding or materially changing wiki pages.

### Agent Lane

- Read `agents/CLAUDE.md` before working in `agents/`.
- Agents may read the full repo but may write only under `agents/`.

## Anti-Patterns

- Do not change thesis state directly from raw notes or agent output.
- Do not store canonical facts only in prose when they belong in `data/`.
- Do not treat `agents/` output as canonical truth.
