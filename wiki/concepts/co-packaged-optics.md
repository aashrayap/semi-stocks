---
title: Co-Packaged Optics (CPO)
tags: [optics, cpo, networking, bottleneck, next]
sources: [../data/thesis.yaml]
created: 2026-04-07
updated: 2026-04-07
---

# Co-Packaged Optics (CPO)

As AI clusters scale to tens of thousands of GPUs, copper cables between racks can't keep up — too slow, too much heat. CPO replaces copper with laser light by integrating optical engines directly onto the chip package.

## Why It's Next (Not Now)

- CPO market projected at $20B by 2036, 37% CAGR
- Rubin Ultra NVL576: CPO between racks — explicitly low volume / test only
- Feynman NVL1152: CPO between racks, copper within rack (base case)
- Jensen at GTC26: "NVL1152 will be all CPO"
- 448G SerDes challenges (shoreline, reach, power) favor CPO over copper at next speed step
- Nvidia Spectrum-X and Quantum-X Photonics built on TSMC SoIC 3D

## Timeline (from GTC26)

| Generation | Scale-Up | Scale-Out |
|------------|----------|-----------|
| NVL72 (Blackwell) | Copper | Pluggable |
| NVL144 (Rubin Ultra) | Copper OR Copper+CPO | Pluggable |
| NVL1152 (Feynman) | All CPO | CPO |

## Key Nuance

Volume CPO is a Feynman story (2028+), NOT Rubin Ultra. Inside every rack through NVL1152 remains copper. This means copper connector companies (ALAB, SMTC) have a longer runway than the CPO hype suggests.

## Source Positioning

| Ticker | Role | Leopold | Baker |
|--------|------|---------|-------|
| COHR | Optical engines | $89M | $228M |
| LITE | Optical engines | $479M | $141M |
| ALAB | Retimers/signal integrity (copper persistence) | — | $268M |
| SMTC | Signal integrity ICs | — | $51M |

CPO winners will be whoever integrates optical engines on-package — COHR and LITE are best positioned but volume revenue is years away.

See also: [[concepts/pluggable-optics]], [[concepts/bottleneck-cascade]]
