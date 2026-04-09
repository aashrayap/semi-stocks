# semi-stocks

Investment research repo for tracking AI infrastructure bottleneck rotation with supply-chain telemetry, high-conviction fund positioning, and earnings evidence.

## Core Thesis

AI compute demand is routinely underestimated. Suppliers build "X minus 1" of required capacity, bottlenecks shift in sequence, and the edge is spotting the next binding constraint before consensus.

| Stage | Status | What matters now |
|---|---|---|
| Memory supercycle | Active | Peak-shortage phase; watch pricing and hedge signals |
| N3 logic wafers | Active | Capacity is tight through 2027; compare demand against fab response |
| Pluggable optics | Active | Current overlap zone across core sources; revenue is already flowing |
| Co-packaged optics | Next | Track technical progress, not near-term volume claims |
| EUV tools | Next | Pre-cycle watchlist tied to fab buildout ceilings |

Live status, dates, and ticker mapping live in `data/thesis.yaml`.

## Truth Path

```text
external evidence
  -> wiki/raw/
  -> wiki/sources/ or wiki/concepts/
  -> data/companies/ or data/sources/
  -> data/thesis.yaml
  -> src/synthesis.py / src/report.py
  -> reports/latest.html
```

`agents/` is a sidecar lane that can read the repo but is not canonical truth until human review promotes changes.

## Current Priorities

- Test the report path end to end.
- Upgrade the 13F pipeline with automated EDGAR ingest and options stripping.
- Work the next catalysts: ASML on 2026-04-15, TSM on 2026-04-16, and INTC on 2026-04-23.
- Add earnings-calendar and source-change detection automation.

See `TODO.md` for the live backlog.

## Reading Map

- `ash.md` - human-first overview of how to iterate on the repo
- `TODO.md` - current priorities and milestones
- `data/thesis.yaml` - thesis control plane, earnings dates, ticker map
- `wiki/concepts/bottleneck-cascade.md` - thesis overview
- `wiki/concepts/source-triangulation.md` - how SemiAnalysis, Leopold, and Baker fit together
- `data/research/earnings-pipeline.md` - canonical earnings and 13F funnel
- `wiki/schema.md` - wiki rules and bookkeeping
- `agents/README.md` - sidecar automation lane

## Iteration Rules

- Use `wiki/` to explain and `data/` to remember what is true.
- Update `data/thesis.yaml` only when structured evidence changes stage status, dates, or ticker mapping.
- Do not create a third hand-maintained truth lane; reports and automation should derive from canonical inputs.
