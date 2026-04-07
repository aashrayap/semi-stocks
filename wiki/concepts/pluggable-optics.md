---
title: Pluggable Optics (Scale-Out)
tags: [optics, pluggable, networking, bottleneck]
sources: [../data/thesis.yaml]
created: 2026-04-07
updated: 2026-04-07
---

# Pluggable Optics (Scale-Out)

Pluggable optical transceivers connect GPU racks to each other over fiber. Every NVL72/NVL144/NVL288 rack Nvidia ships uses pluggable optics for scale-out networking. Revenue is flowing NOW.

## Why It's a Bottleneck

- Every rack has OSFP cages for inter-rack connectivity
- LPX rack: 8x OSFP cages per tray for C2C
- Spectrum-X Ethernet scale-out connects LPU<>GPU in disaggregated decode
- Blackwell NVL576 prototype "Polyphe" uses pluggable optics between racks
- Vera ETL256: 32 front-facing OSFP cages per rack for pod connectivity
- 800G/1.6T transceivers are the current shipping product
- NVIDIA networking revenue hit $11B quarterly (+3.5x YoY, Q4 FY2026) — Jensen called Spectrum-X "a home run"

## The Consensus Zone

This is the ONLY bottleneck where all three sources agree. It's the highest-conviction, lowest-divergence-risk zone in the entire thesis.

## Source Positioning

| Ticker | Role | Leopold | Baker |
|--------|------|---------|-------|
| COHR | 800G/1.6T transceivers | $89M | $228M |
| LITE | 800G/1.6T transceivers | $479M | $141M |
| CIEN | Optical networking switches | — | $334M |

## Relationship to CPO

Pluggable optics is the current trade. [[concepts/co-packaged-optics]] is the next evolution (2028+). Copper handles inside-rack connections today; pluggable handles rack-to-rack. When distances and bandwidth exceed pluggable limits, CPO takes over.

Jensen at GTC26: copper scales to NVL144 (maybe 288). NVL1152 (Feynman) will be "all CPO." But pluggable and copper consumption still grows because there are 5 different rack types, all needing connectivity.

## Earnings Confirmation

- **CRWV Q4 2025:** Every NVL72 rack deployed uses pluggable optics for scale-out. 100K+ GPUs deployed in Q4 = significant transceiver demand.
- **NVDA Q4 FY2026:** Networking revenue $11B (+3.5x YoY). Grace Blackwell = ~2/3 of DC revenue, all rack-scale with optics. "We ship racks of computers."

See also: [[concepts/bottleneck-cascade]], [[concepts/co-packaged-optics]], [[sources/semianalysis-signals]], [[sources/crwv-q4-2025]], [[sources/nvda-q4-fy2026]]
