---
title: Source Triangulation
tags: [workflow, thesis, sources, positioning]
sources: [sources/leopold-q4-2025.md, sources/baker-q4-2025.md, sources/semianalysis-signals.md]
created: 2026-04-09
updated: 2026-04-09
---

# Source Triangulation

The repo's core signal comes from combining three different lenses on the same AI infrastructure stack.

| Lens | What it sees first | Useful for | Failure mode |
|---|---|---|---|
| SemiAnalysis | Physical bottlenecks, capacity, demand | Timing the real constraint | Can be early before the market expresses it |
| Leopold | High-conviction capital expression around AI timelines | Seeing where an aggressive bull rotates | Can over-index to deployment, power, and concentration |
| Baker | Cycle-aware semiconductor positioning with hedges | Seeing where scarcity is investable versus over-earned | Can be right on structure but early on cycle turns |

## Interpretation Grid

| Pattern | Meaning | Default action |
|---|---|---|
| Three-way agreement | Physical constraint and capital expression line up | Highest-conviction zone; deepen evidence and monitor sizing and risk |
| SemiAnalysis + one fund | Likely emerging bottleneck or timing disagreement | Check earnings, valuation, and catalyst timing to explain the third source |
| Leopold vs Baker divergence | Active debate about the current binding constraint | Treat as a research priority and focus on falsifying catalysts |
| Funds agree without SemiAnalysis support | Positioning may be ahead of telemetry or consensus is crowded | Inspect expectations and crowding before sizing |
| SemiAnalysis alone | Possible early signal | Collect company evidence before thesis promotion |

## Current Read

- Shared agreement zone: optical interconnect, especially COHR and LITE.
- Main disagreement: power and deployment versus semiconductor supply chain.
- SemiAnalysis keeps the repo anchored to the physical world when capital allocators disagree.

## Iteration Rule

1. Capture the raw source or durable upstream artifact.
2. Summarize it in `wiki/sources/` or connect it to an existing `wiki/concepts/` page.
3. Promote durable facts to `data/sources/`, `data/companies/`, or both.
4. Update `data/thesis.yaml` only when the structured evidence changes state, dates, or ticker mapping.

When the same point appears in both prose and YAML, `data/` wins.

See also: [[concepts/bottleneck-cascade]], [[concepts/research-control-plane]], [[sources/leopold-q4-2025]], [[sources/baker-q4-2025]], [[sources/semianalysis-signals]]
