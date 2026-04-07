# SemiAnalysis Monitor — 2026-04-07

**Check window:** Apr 5–7, 2026  
**Result:** No new articles confirmed strictly within the 2-day window. Most recent confirmed publication: **Apr 3, 2026** (memory capex analysis, via startupnews.fyi). Data points from that article not yet captured in signals.yaml are actionable and logged below.

**MNPI context:** Use SemiAnalysis for direction; discount magnitude by 6-12 months. 40% of revenue from hedge fund clients.

---

## New Data Points (Apr 3 Article — Not Previously in signals.yaml)

**Source:** startupnews.fyi coverage of SemiAnalysis memory capex report  
**URL:** https://startupnews.fyi/2026/04/03/memory-will-consume-30-of-hyperscaler-data-center-spending-this-year-a-4x-increase-over-2023-nvidia-gets-preferential-supply-terms-well-below-standard-market-rates-says-analyst-firm/

### Key Claims

1. **Nvidia "VVP" (Very Very Preferred) DRAM pricing** — Nvidia receives memory supply at significantly below-market rates. HBM and DRAM vendors prioritize Nvidia allocation to protect the GPU ecosystem.

2. **AMD structural disadvantage** — AMD does NOT receive preferential memory pricing. Rising HBM/DRAM costs compress AMD GPU margins more than Nvidia's.

3. **B200 ASP +20% by year-end** — Nvidia is expected to raise B200 pricing ~20% in H2 2026, consistent with supply tightness and demand momentum.

4. **LPDDR5 contract prices tripled** since Q1 2025; spot prices estimated at $10+/GB.

5. **HBM undersupplied through 2027** — all three vendors (SK Hynix, Samsung, Micron) remain sold out; no meaningful new capacity until HBM4 ramp (late 2026–2027).

---

## Bottleneck Cascade Mapping

| Claim | Cascade Node | Status | Direction |
|-------|-------------|--------|-----------|
| HBM undersupplied through 2027 | Memory supercycle | active | **Strengthens** |
| LPDDR5 spot $10+/GB (+3x) | Memory supercycle | active | **Strengthens** |
| Nvidia VVP pricing below market | N3 logic / GPU moat | active | **New nuance** — moat wider than modeled |
| AMD margin compression from memory costs | N3 logic | active | **New risk** — AMD GPU margin headwind |
| B200 ASP +20% H2 2026 | N3 logic | active | **Strengthens** NVDA pricing power |

---

## Thesis Alignment Assessment

### Strengthens
- **Memory active thesis (MU, SNDK):** Undersupply through 2027 is stronger than current thesis language implies (current: "sold out through 2026"). Update warranted.
- **NVDA pricing power:** VVP supply terms + B200 ASP raise = moat wider than modeled. Baker's $1B+ NVDA long looks well-supported.
- **N3 scarcity thesis:** B200 +20% ASP is a direct read-through — Nvidia only raises prices when supply is genuinely constrained.

### Contradicts / Introduces Risk
- None that directly contradict existing positions.

### New Signal Worth Watching
- **AMD GPU margin risk:** AMD does not have VVP pricing. If HBM costs rise another 2x in 2027 (as SemiAnalysis projects), AMD GPU gross margins get structurally squeezed. This is a short thesis on AMD GPUs or at minimum a reason to underweight vs. Nvidia. Neither Leopold nor Baker appears significantly long AMD GPUs.

---

## Actions Taken

- `signals.yaml`: Added Apr 3 entry with VVP pricing, AMD margin risk, B200 ASP, LPDDR5 data points.
- `thesis.yaml`: Extended memory supercycle undersupply horizon from "through 2026" to "through 2027"; added note on Nvidia VVP competitive moat in N3 logic node.
- No position changes warranted — signals strengthen existing longs (MU, SNDK, NVDA).
