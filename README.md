# semi-stocks

Investment research framework tracking AI infrastructure bottleneck rotation using supply chain data and high-conviction fund positioning.

## Thesis

AI compute demand is chronically underestimated by the semiconductor supply chain. Every supplier builds "X minus 1" of what's needed. Bottlenecks shift in sequence — whoever identifies the *next* binding constraint before consensus captures outsized returns.

```
BOTTLENECK CASCADE (confirmed sequence)
════════════════════════════════════════════════════════════════════

  2023          2024           2025           2026-27        2028-30
  CoWoS         Power/DC       Memory         N3 logic       EUV tools
  packaging     buildout       supercycle     wafers         (ASML ceiling)
  ✅ played out  ✅ played out   🔴 active       🟡 emerging     🟡 next
```

## Quality Sources

### 1. SemiAnalysis (Dylan Patel)
- **What:** Proprietary supply chain data — tracks every data center, fab, tool order, wafer allocation globally
- **Edge:** Only source with bottom-up models for TSMC wafer allocation, ASML tool shipments, HBM capacity by vendor, and hyperscaler CapEx breakdown
- **Key calls:** Memory crunch (Sep 2024, 12mo early), CoWoS bottleneck (2023), power crisis (2024)
- **Current warnings:**
  - 30% of Big Tech's $600B CapEx goes to memory
  - Smartphone volumes dropping from 1.4B to 500-600M units (DRAM demand destruction)
  - N3 wafers at 100%+ utilization H2 2026
  - ASML EUV ceiling: ~100 tools/yr by 2030, 3.5 tools per gigawatt
  - Cleanroom/fab space is the current physical bottleneck (2yr build time)
- **URL:** [semianalysis.com](https://newsletter.semianalysis.com)

### 2. Leopold Aschenbrenner — Situational Awareness LP
- **What:** $5.5B hedge fund. Former OpenAI researcher. Wrote "Situational Awareness" (AGI by ~2027 thesis)
- **Edge:** Highest conviction on AI timelines of any public fund manager. Only SemiAnalysis client who says numbers are "too low"
- **Track record:** +47% net H1 2025 vs S&P +6%. Grew from $254M to $5.5B in ~1 year
- **Current positioning (Q4 2025 13F):**
  - **EXITED NVDA and AVGO entirely** — moved down-stack from chips to power/infra
  - Top 5: CoreWeave ($1.2B), Bloom Energy ($911M), Intel calls ($749M), Lumentum ($479M), Core Scientific ($419M)
  - ~15% in bitcoin miners converting to AI DCs (CORZ, IREN, APLD, CIFR, RIOT, HUT, BTDR, CLSK, BITF)
  - ~22% in power/energy (BE, EQT, SEI, LBRT, PUMP, BW)
  - Storage: SanDisk +816% increase
- **Signal:** Power is THE bottleneck now, not chips
- **13F:** [WhaleWisdom](https://whalewisdom.com/filer/situational-awareness-lp) | [13f.info](https://13f.info/13f/000204572426000002-situational-awareness-lp-q4-2025)

### 3. Gavin Baker — Atreides Management
- **What:** $8.2B crossover fund. NVIDIA's first major institutional investor 20+ years ago
- **Edge:** Deep semiconductor supply chain understanding. Public commentary via podcasts provides thesis transparency
- **Current positioning (Q4 2025 13F):**
  - **Massive NVDA long** ($1B+ including $902M in NEW call options) — opposite of Leopold
  - Supply chain stack: Coherent ($394M), Micron ($411M), Pure Storage ($381M), Ciena ($334M), Astera Labs ($268M)
  - **Exited AMD and META entirely** — winner-take-most in GPUs, consolidating around NVDA
  - QQQ puts ($2.2B notional) as macro hedge
  - New: WIX, MSFT, GNRC
- **Signal:** Semiconductor supply chain (optical, memory, storage) is the bottleneck, not power
- **13F:** [WhaleWisdom](https://whalewisdom.com/filer/atreides-management-lp) | [InsiderMonkey](https://www.insidermonkey.com/hedge-fund/atreides+management/1215/holdings/)

## How They Diverge

| Dimension | Leopold | Baker |
|-----------|---------|-------|
| Primary bottleneck | Power generation | Semiconductor supply chain |
| NVIDIA | **Fully exited** | **$1B+ long with calls** |
| GPU cloud (CRWV) | #1 position ($1.2B) | Not held |
| Bitcoin miners | ~$750M across 8 names | Not held |
| Power/energy | ~$1.2B (BE, EQT, etc.) | Not held |
| Memory | Short Micron thesis | Long Micron ($411M) |
| Optical interconnect | LITE ($479M), COHR ($89M) | COHR ($394M), LITE ($141M), CIEN ($334M) |
| Hedging | No visible hedges | QQQ puts ($2.2B) |
| Concentration | 25 positions, top 5 = 68% | 56 positions, more diversified |

**Overlap:** Only 3 shared tickers — COHR, LITE, INTC. Both agree optical interconnect is critical. They disagree on whether chips or power is the binding constraint.

## Actionable Framework

The meta-principle: **buy the next bottleneck before it becomes consensus, sell the current one as it becomes consensus.**

```
IF you believe power is the binding constraint (Leopold's view):
  → BE, bitcoin miners (CORZ, IREN, CIFR), EQT, CRWV

IF you believe semicon supply chain is binding (Baker's view):
  → NVDA calls, COHR, CIEN, ALAB, MU, PSTG

IF you believe both are right on different timescales:
  → Power names NOW, rotate to ASML/equipment 2027-28

Overlap zone (both agree):
  → COHR, LITE (optical interconnect)
```

## Research Pipeline

Research flows through a layered funnel — wide at ingest, narrow at thesis.

```
wiki/raw/              → wiki/sources/           → data/companies/        → data/thesis.yaml
(transcripts, filings)   (synthesized pages)       (structured YAML)        (cascade updates)
~20 companies            ~12-15 companies          ~5-8 companies           only when status shifts
```

- **wiki/raw/** — Immutable source material. Full earnings transcripts, SEC filings, articles. Cheap to store.
- **wiki/sources/** — Synthesized knowledge pages. Key metrics, guidance claims, notable quotes, wikilinks to concepts. Self-contained for most queries.
- **data/companies/** — Structured analysis for high-conviction names. Quarterly YAML with financials, forward claims (verifiable with `status: pending|confirmed|missed`), thesis signals, fund positioning cross-reference.
- **data/thesis.yaml** — Cascade status. Updated only when earnings data actually shifts a bottleneck.

See `wiki/schema.md` for wiki conventions and `CLAUDE.md` for the full earnings pipeline process.

## Data Refresh Cadence

- **13F filings:** Quarterly (45 days after quarter end). Next: ~May 15, 2026
- **SemiAnalysis:** Continuous newsletter + paid data products
- **Earnings calls:** Track ASML, TSM, SK Hynix, MU for supply chain signals; see CLAUDE.md § Earnings Pipeline
 