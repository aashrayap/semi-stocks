# Wiki Log — semi-stocks

Append-only record of wiki activity. Each entry starts with `## [date] action | description`.

---

## [2026-04-08] ingest | MU / INTC / TSM / LITE deep-dive catch-up

Closed the remaining deep-dive alignment gaps by adding full raw/source/structured company coverage for MU Q2 FY2026, INTC Q4 2025, TSM Q4 2025, and LITE Q2 FY2026.

Updated concept pages so the new company signals resolve into the existing thesis graph:
- `concepts/memory-supercycle.md` now includes Micron's record quarter and sharp Q3 guide-up
- `concepts/n3-wafer-crunch.md` now includes direct TSMC and Intel confirmation
- `concepts/foundry.md` now anchors Intel optionality and TSMC scale in concrete numbers
- `concepts/pluggable-optics.md` and `concepts/co-packaged-optics.md` now include Lumentum's current optical acceleration and early CPO booked-demand signal

Updated the thesis control plane to the latest confirmed investor-relations dates:
- TSM next earnings: 2026-04-16
- INTC next earnings: 2026-04-23
- LITE next earnings: 2026-05-05

MU's next earnings date remains 2026-06-25 in the control plane pending an official Micron IR announcement.

---

## [2026-04-08] update | Alignment burn-down + raw/source restoration

Restored the `wiki/raw/` layer after migration left the directory absent from the worktree. Added restored raw source bundles for CRWV Q4 2025 and NVDA Q4 FY2026 so existing wiki source pages once again resolve to a canonical upstream artifact.

Added missing concept pages to match the control plane in `data/thesis.yaml`: `gpu-cloud`, `power`, `foundry`, `copper-signal-integrity`, and `euv-tools`. Updated linked concept/source pages so the graph reflects the same bottleneck vocabulary used by the ticker map.

Updated `data/thesis.yaml` to move ASML's next earnings date from 2026-04-16 to 2026-04-15 based on the official ASML investor relations calendar.

Alignment warnings reduced from 14 to 4. Remaining gaps are the still-missing deep-dive company YAMLs for MU, INTC, TSM, and LITE.

---

## [2026-04-08] ingest | Coherent Q2 FY2026 Earnings

Third earnings pipeline run. Three-layer funnel:
- **Raw:** `raw/cohr-q2-fy2026-earnings-release.md` (official Coherent earnings release, primary-source bundle)
- **Source:** `sources/cohr-q2-fy2026.md` (synthesized: metrics, guidance, thesis signal, Baker/Leopold agreement)
- **Structure:** `data/companies/COHR/q2_fy2026.yaml` (financials, guidance claims, thesis signal, positioning)

Key thesis signals: datacenter and communications demand remained strong, margins expanded, and management kept ramping capacity to support optical demand. COHR remains the cleanest agreement zone across Leopold, Baker, and SemiAnalysis.

---

## [2026-04-07] update | Report restructure + cycle risk integration

Restructured report from 9 sections → 5 (3 main + summary + collapsed drift):
1. Summary (+ cycle risk sentence, Baker hedge ratio)
2. Cascade + Cycle Risk (merged cascade, explainers→one-liners, cycle phase/action/flags)
3. Positions + Signals (merged agreement map + divergences inline)
4. Earnings Dashboard (merged forward claims + thesis signals + SemiAnalysis per ticker)
5. Drift (collapsed `<details>`, count badge only)

Added to `thesis.yaml`: `cycle_phase`, `cycle_signal`, `cycle_risk_flags` per cascade stage. `baker_hedge_ratio` as tracked metric (0.70, trend: increasing).

Added to `synthesis.py`: `cycle_assessment()`, `baker_hedge_ratio()`, `earnings_dashboard()`, `BOTTLENECK_ONE_LINERS`.

Updated `README.md` actionable framework: two dimensions (which bottleneck + when in cycle).

---

## [2026-04-07] query → output | Baker's cyclicality thesis — "every shortage followed by a glut"

Filed to `outputs/baker-cyclicality-thesis.md`. Research dispatched across 7 parallel subagents covering: Memory (MU), Foundry (TSM), Equipment (ASML/LRCX/AMAT), Broadcom (AVGO), Auto/Analog (TXN/ON/NXPI/ADI), GPU (NVDA/AMD), and Baker's public commentary. Synthesized evidence matrix, P/E compression data, lead time signals, and counter-arguments. Key finding: Baker's framework confirmed across all subsectors except AVGO (partial exception due to software mix and supply discipline). TXN is the single strongest proof point — P/E 16x at peak earnings, 38x at trough, stock higher during glut.

---

## [2026-04-07] query → output | NVDA pre-earnings swing trade thesis

Filed `outputs/nvda-swing-trade-thesis.md`. Query synthesized wiki sources (NVDA Q4 FY2026 earnings, Baker/Leopold positioning, SemiAnalysis signals, bottleneck cascade, token economics) with live market research (price history, technicals, options data, analyst consensus).

Key findings: $170 support confirmed (3 tests), $185-190 resistance confirmed (death cross). Forward P/E 21x on 73% growth = fundamental floor. Iron condor ($170/$190 short strikes, May 16 expiry) + directional swing trade ($171 entry, $183-185 target, $165 stop). Hard exit by May 20 before earnings.

Also added `next_earnings` field to all tickers in `thesis.yaml` and an Earnings column to the report source agreement map (color-coded: red <=7d, orange <=21d).

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
