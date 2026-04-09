# semi-stocks

Research repo tracking AI infrastructure bottleneck rotation. Start each session at `TODO.md`. Treat `README.md` as the landing page and use the docs below for canonical detail.

## Repo Map

- `data/thesis.yaml` - bottleneck control plane, next earnings dates, ticker map
- `data/research/earnings-pipeline.md` - canonical ingest and promotion path
- `data/research/13f-pipeline-design.md` - 13F automation direction
- `wiki/schema.md` - wiki rules and bookkeeping
- `wiki/concepts/bottleneck-cascade.md` - thesis overview
- `wiki/concepts/source-triangulation.md` - how SemiAnalysis, Leopold, and Baker fit together
- `agents/` - sidecar lane; non-authoritative until human review promotes changes

<important if="you need orientation before acting">
Read in order: `TODO.md`, `data/thesis.yaml`, `wiki/concepts/bottleneck-cascade.md`, `wiki/concepts/source-triangulation.md`, and `data/research/earnings-pipeline.md`.
</important>

<important if="writing or updating canonical research">
Truth path: `wiki/raw/` -> `wiki/sources/` or `wiki/concepts/` -> `data/companies/` or `data/sources/` -> `data/thesis.yaml` -> reports.
`data/` is the final authority when prose and structure differ. Do not create a new hand-maintained truth lane.
</important>

<important if="ingesting earnings or transcripts">
Follow `data/research/earnings-pipeline.md`. Score prior `forward_claims` first. Deep-dive names: CRWV, NVDA, MU, COHR, INTC, TSM, LITE.
</important>

<important if="ingesting or analyzing a 13F">
Cross-check against SEC EDGAR and at least two aggregators before promotion. Divergence between Leopold and Baker is a thesis signal, not noise.
</important>

<important if="editing wiki pages">
Read `wiki/schema.md` first. Update `wiki/index.md` and `wiki/log.md` when adding or materially changing wiki pages.
</important>

<important if="working under agents/">
Read `agents/CLAUDE.md`. Agents may read the full repo but may write only under `agents/`. Agent output stays non-canonical until human review promotes it.
</important>
