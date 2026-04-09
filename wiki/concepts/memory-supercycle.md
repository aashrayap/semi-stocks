---
title: Memory Supercycle
tags: [memory, hbm, dram, bottleneck]
sources: [../data/thesis.yaml, ../data/sources/semianalysis/signals.yaml]
created: 2026-04-07
updated: 2026-04-08
---

# Memory Supercycle

Every AI chip needs memory (DRAM/HBM) to hold the data it's processing. HBM (High Bandwidth Memory) is special memory stacked in layers and bonded directly to the GPU — it's 85% less dense than regular DRAM and much harder to make.

## Why It's a Bottleneck

AI is consuming so much memory that there isn't enough left for phones, PCs, and other devices. The result:
- DRAM contract prices surged +90-95% in a single quarter (Q1 2026, TrendForce)
- DDR4 spot price ($2.10/Gbit) now exceeds HBM3e ($1.70/Gbit) — unprecedented inversion
- 30% of Big Tech's $650B CapEx goes to memory
- HBM revenue projected at 41% of total DRAM by 2026
- All vendors (SK Hynix, Samsung, Micron) sold out through 2026
- Smartphone volumes declining from 1.4B to 500-600M units — DRAM demand destruction freeing supply for AI
- NVIDIA carries $21.4B inventory including significant HBM stockpile (Q4 FY2026)

## Source Positioning

- **Baker:** Long MU ($411M) + put hedge. Believes memory is binding.
- **Leopold:** Exited MU puts in Q4 2025. Not actively positioned in memory.
- **SemiAnalysis:** Flagged memory crunch Sep 2024, 12 months early.

## Key Tickers

| Ticker | Role | Held By |
|--------|------|---------|
| MU | DRAM/HBM manufacturer | Baker |
| SNDK | Storage/NAND | Leopold (+816% QoQ) |

## Earnings Confirmation

- **CRWV Q4 2025:** Every GPU CRWV deploys needs HBM. $30-35B capex = substantial HBM demand pull-through.
- **NVDA Q4 FY2026:** $21.4B inventory (HBM stockpile). Every GPU shipped needs HBM — NVIDIA GPU volumes are the primary demand driver.
- **MU Q2 FY2026:** Revenue reached $23.86B, non-GAAP gross margin hit 74.9%, and Q3 guidance moved to $33.5B +/- $750M at roughly 81% gross margin. Management explicitly cited strong demand and tight industry supply.

That Micron print matters because it turns the memory thesis from channel checks and third-party signals into direct company evidence. Baker's long-plus-put posture now reads like peak-shortage positioning, not doubt that the shortage exists.

See also: [[concepts/bottleneck-cascade]], [[concepts/n3-wafer-crunch]], [[sources/crwv-q4-2025]], [[sources/nvda-q4-fy2026]], [[sources/mu-q2-fy2026]]
