---
title: "Semi-stocks Repository Review"
tags: [meta, repository-review, workflow, risk, research-system]
sources: [raw/semi-stocks-repository-review-2026-04-09.md]
created: 2026-04-09
updated: 2026-04-09
source_created: 2026-04-09
---

# Semi-stocks Repository Review

This review treats the repo as an emerging institutional research system, not just a thesis notebook. The verdict is favorable on thesis structure and claim accountability, but clear about what is still missing around that core.

## Bottom Line

The repo is already strong at:
- expressing the bottleneck-rotation thesis as a linked graph
- tying company earnings into verifiable forward claims
- comparing Baker, Leopold, and SemiAnalysis as distinct lenses

The repo is still weak at:
- measuring what the market already expects
- tracking real-world bottleneck telemetry outside a single synthesized narrator
- controlling portfolio-level risk, crowding, and scenario exposure

## Highest-Priority Gaps

| Gap | Why it matters |
|------|----------------|
| Demand-side actuals and guidance | Distinguishes real shortage from pull-forward or digestion |
| Tape, price, and volume | Needed for timing, backtests, and separating thesis failure from positioning noise |
| Consensus estimates and revision tracking | Semiconductor stocks move on expectation changes, not just prints |
| Primary industry indicators | Needed to confirm scarcity independently of a single narrator |
| Geopolitical and regulatory tracker | Export controls and policy shifts can reroute the whole cascade |

## Missing System Layers

The review argues the thesis needs a control plane around it:

1. **Expectations layer**: consensus, revisions, implied expectations, flows, and crowding
2. **Telemetry layer**: supply-chain data plus physical-world indicators like grid load, interconnection queues, data-center capacity, and component pricing
3. **Portfolio/risk layer**: factor exposure, scenario stress tests, liquidity limits, and event-risk sizing
4. **Workflow cadence**: pre-earnings setup, post-earnings diffing, between-quarter calendars, and scored postmortems

Those ideas are captured in [[concepts/research-control-plane]].

## Implications For This Repo

- [[concepts/bottleneck-cascade]] is a good answer to "where is the bottleneck?"
- The missing layers answer "what is priced?", "what is changing in the real world?", and "how much risk should the portfolio run?"
- [[concepts/power]] is the clearest example where physical telemetry matters beyond semiconductor commentary
- Existing `data/companies/` pages already hold some expectations data, but not as a system-wide layer

## Proposed Priority Order

The review's most urgent additions are:

1. an explicit expectations layer
2. broader bottleneck telemetry
3. portfolio/risk controls
4. repeatable research cadence around earnings and between-quarter indicators

This source is meta-research. It does not directly change `data/thesis.yaml`, but it changes how future evidence should be gathered and interpreted.

See also: [[concepts/research-control-plane]], [[concepts/bottleneck-cascade]], [[concepts/power]], [[outputs/baker-cyclicality-thesis]]
