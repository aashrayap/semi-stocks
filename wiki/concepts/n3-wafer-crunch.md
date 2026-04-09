---
title: N3 Wafer Crunch
tags: [tsmc, n3, wafers, bottleneck, foundry]
sources: [../data/thesis.yaml, ../data/sources/semianalysis/signals.yaml]
created: 2026-04-07
updated: 2026-04-08
---

# N3 Wafer Crunch

N3 refers to TSMC's 3-nanometer manufacturing process — the most advanced way to make chips. Every major AI accelerator is moving to N3 simultaneously in 2026, creating a capacity crunch.

## Why It's a Bottleneck

- AI already consumes 60% of TSMC N3 output (2026), projected 86% by 2027
- N3 utilization at 100%+ in H2 2026
- All major accelerators moving to N3 simultaneously: Nvidia Rubin, Google TPU v7/v8, Amazon Trainium3, AMD MI350X
- CPUs competing for same N3 capacity: Venice, Diamond Rapids, Vera
- Reallocating just 5% of smartphone N3 wafers = ~100K Rubin GPUs
- AI chips are literally crowding out smartphone chips (Apple, Qualcomm, MediaTek)
- NVIDIA supply commitments doubled $50.3B → $95.2B QoQ, capacity secured through CY2027 (Q4 FY2026)
- Vera Rubin samples shipped, production H2 2026 — six new chips this cycle all on N3

## Source Positioning

- **Baker:** Massive NVDA long ($1B+ including $902M in new call options). If supply is constrained, the company with strongest demand has pricing power. Also long AVGO.
- **Leopold:** Holds INTC calls ($749M) but exited NVDA entirely. Betting on Intel as alternative N3 supplier (Intel Foundry Services).
- **SemiAnalysis:** Flagged N3 as binding. Originally sequenced after memory but data shows both binding simultaneously.

## Key Tickers

| Ticker | Role | Held By |
|--------|------|---------|
| TSM | N3 manufacturer (monopoly) | Neither (too consensus?) |
| NVDA | Largest N3 consumer | Baker ($1B+) |
| AVGO | N3 consumer (networking) | Baker |
| INTC | Alternative foundry play | Leopold ($749M calls) |
| TSEM | Specialty foundry | Leopold ($85M) |

Alternative manufacturing exposure beyond TSMC lives in [[concepts/foundry]]. INTC is the leading-edge optionality trade; TSEM is the specialty foundry adjacency.

## Earnings Confirmation

- **CRWV Q4 2025:** Delivered 50K GB200s in Q4 to single customer. Nvidia GPUs "remain in short supply." $30-35B capex = enormous chip demand.
- **NVDA Q4 FY2026:** Rubin moving to N3, competing with TPU v7/v8, Trainium3, MI350X for TSMC capacity. Supply commitments nearly doubled. Six new chips all on N3.
- **TSMC Q4 2025:** Revenue reached $33.73B, 3nm rose to 28% of wafer revenue, advanced nodes reached 77%, and Q1 guidance stepped up again to $34.6B-$35.8B. Management also set a $52B-$56B 2026 capital budget.
- **INTC Q4 2025:** Intel's first 18A products launched and Intel Foundry posted $4.5B of revenue, but Q1 guidance stayed soft at $11.7B-$12.7B and management said supply improves only after Q1. Alternative capacity still is not relieving the main shortage yet.

The key read is that TSMC still looks fully absorbed while Intel still looks transitional. That combination reinforces the repo's view that the N3 bottleneck remains active even as the first alternative-capacity pathways start to form.

See also: [[concepts/bottleneck-cascade]], [[concepts/memory-supercycle]], [[concepts/pluggable-optics]], [[concepts/foundry]], [[sources/crwv-q4-2025]], [[sources/nvda-q4-fy2026]], [[sources/tsm-q4-2025]], [[sources/intc-q4-2025]]
