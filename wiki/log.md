# Wiki Log — semi-stocks

Append-only record of wiki activity. Each entry starts with `## [date] action | description`.

---

## [2026-04-07] update | Concept pages updated with earnings confirmation

Updated 3 concept pages to reflect CRWV Q4 2025 and NVDA Q4 FY2026 earnings signals:
- `concepts/memory-supercycle.md` — added NVIDIA $21.4B HBM inventory signal, earnings confirmation section
- `concepts/n3-wafer-crunch.md` — added NVIDIA supply commitments doubling, Vera Rubin production signal, earnings confirmation section
- `concepts/pluggable-optics.md` — added NVIDIA $11B networking revenue signal, earnings confirmation section

Drift warnings reduced from 11 → 1 (remaining: no dedicated gpu_cloud concept page).

---

## [2026-04-07] ingest | NVIDIA Q4 FY2026 Earnings

Second earnings pipeline run. Full three-layer funnel:
- **Raw:** `raw/nvda-q4-fy2026-transcript.md` (compiled from NVIDIA Newsroom, Motley Fool, Yahoo Finance, Fortune, Ticker Report)
- **Source:** `sources/nvda-q4-fy2026.md` (synthesized: metrics, quotes, guidance, 7 forward claims, bottleneck mapping, Baker/Leopold divergence)
- **Structure:** `data/companies/NVDA/q4_fy2026.yaml` (7 forward_claims with verify_at dates, thesis signals across 4 bottlenecks, product highlights, partnership announcements)

Key thesis signals: $95.2B supply commitments (doubled QoQ), $11B networking quarter validates optics, Rubin production H2 2026 adds N3 pressure. Baker/Leopold NVDA divergence is the clearest thesis disagreement — Baker $1B+ long, Leopold exited.

---

## [2026-04-07] ingest | CoreWeave Q4 2025 Earnings — first earnings pipeline run

First use of the earnings pipeline. Three-layer funnel:
- **Raw:** `raw/crwv-q4-2025-transcript.md` (full earnings call transcript, FactSet/CallStreet corrected)
- **Source:** `sources/crwv-q4-2025.md` (synthesized: metrics, quotes, guidance claims, bottleneck mapping, Leopold/Baker divergence)
- **Structure:** `data/companies/CRWV/q4_2025.yaml` (9 forward_claims with verify_at dates, thesis signals across 5 bottlenecks)

Moved from 2026/wiki/ to semi-stocks/wiki/ (correct location per architecture).

## [2026-04-07] init | Semi-stocks wiki scaffolded

Created wiki structure inside semi-stocks/. Thesis-linked to `data/thesis.yaml`.

Seed content migrated from existing README.md narrative, thesis.yaml signals, and synthesis.py BOTTLENECK_EXPLAINERS.

**Concept pages created:** bottleneck-cascade, memory-supercycle, n3-wafer-crunch, pluggable-optics, co-packaged-optics, token-economics
**Source pages created:** leopold-q4-2025, baker-q4-2025, semianalysis-signals
