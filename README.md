# semi-stocks

Investment research framework tracking AI infrastructure bottleneck rotation using supply chain data and high-conviction fund positioning.

## Thesis

AI compute demand is chronically underestimated by the semiconductor supply chain. Every supplier builds "X minus 1" of what's needed. Bottlenecks shift in sequence — whoever identifies the *next* binding constraint before consensus captures outsized returns.

```
BOTTLENECK CASCADE (confirmed sequence + cycle phase)
════════════════════════════════════════════════════════════════════════════

  2023          2024           2025-26        2025-27        2028-30
  CoWoS         Power/DC       Memory         N3 logic       EUV tools
  packaging     buildout       supercycle     wafers         (ASML ceiling)
  ✅ resolved    ✅ post-peak    🔴 PEAK SHORT   🟠 mid short    ⚪ pre-cycle
                                → hedge now    → long+hedge    → watch
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

Two orthogonal dimensions drive positioning:

1. **Which bottleneck** (rotation) — buy the *next* constraint before consensus, sell as it becomes consensus
2. **When in the cycle** (timing) — Baker's "iron law": every shortage is followed by a glut. Buy at high P/E (trough earnings), sell/hedge at low P/E (peak earnings). Lead times are the signal.

```
DIMENSION 1: WHICH BOTTLENECK

IF you believe power is the binding constraint (Leopold's view):
  → BE, bitcoin miners (CORZ, IREN, CIFR), EQT, CRWV

IF you believe semicon supply chain is binding (Baker's view):
  → NVDA calls, COHR, CIEN, ALAB, MU, PSTG

Overlap zone (both agree):
  → COHR, LITE (optical interconnect)

DIMENSION 2: WHEN IN THE CYCLE (Baker framework)

  Memory (MU):    PEAK SHORTAGE → Long + puts (Baker: $411M common + $200M puts)
  N3 (NVDA/TSM):  MID SHORTAGE  → Long + macro hedge (Baker: $1B NVDA + $2.2B QQQ puts)
  Optics (COHR):  EARLY CYCLE   → Long (revenue just started, no glut history yet)
  Equipment:      PRE-CYCLE     → Watch (ASML record bookings = approach with caution)
```

See `wiki/outputs/baker-cyclicality-thesis.md` for the full evidence base (6 subsectors, P/E data, lead times).

## Repo Architecture

There are two distinct processes in this repo:

1. **Canonical manual/wiki pipeline** — the authoritative path for research facts and thesis state
2. **Agent sidecar pipeline** — a parallel, non-authoritative path for alerts, predictions, drafts, and experiments

```
WIDE EVIDENCE

earnings releases / transcripts / 13Fs / articles / daily notes / calendars
  -> wiki/raw/                    canonical raw evidence (local-first, gitignored)
  -> agents/drafts/earnings/     agent staging only, not canonical

MID SYNTHESIS

wiki/sources/*.md                per-event synthesis
wiki/concepts/*.md               cross-cutting thesis/context pages
wiki/outputs/*.md                filed analysis outputs

STRUCTURED TRUTH

data/sources/*/*.yaml            structured source snapshots
data/companies/<TICKER>/q*.yaml  structured company quarters
data/thesis.yaml                 thesis control plane

DERIVED VIEWS

src/synthesis.py + src/report.py -> reports/latest.html
agents/src/*                     -> agent reports / predictions / backtests
```

## Canonical Manual / Wiki Pipeline

This is the path that should be treated as truth.

```
CANONICAL PIPELINE (authoritative)

Earnings / transcripts / releases / 13Fs / articles
  -> wiki/raw/
     raw evidence only; immutable after capture

  -> wiki/sources/<event>.md
     human-readable synthesis of one earnings event, filing, or source

  -> wiki/concepts/<topic>.md
     optional cross-cutting concept updates when the new evidence changes the graph

  -> data/companies/<TICKER>/q*.yaml    for earnings/company facts
  -> data/sources/<SOURCE>/q*.yaml      for fund/source positioning facts

  -> data/thesis.yaml
     only when structured evidence changes bottleneck state, dates, or ticker map

  -> src/synthesis.py
  -> src/report.py
  -> reports/latest.html
```

### Canonical Layer Responsibilities

| Layer | Role | Authority |
|---|---|---|
| `wiki/raw/` | Raw upstream evidence: transcripts, releases, filing bundles, article captures | Evidence only |
| `wiki/sources/` | Event-level synthesis for humans | Interpretive, but should cite raw |
| `wiki/concepts/` | Cross-cutting compiled knowledge | Interpretive, thesis-linked |
| `data/companies/` | Canonical structured company facts by quarter | Authoritative for company data |
| `data/sources/` | Canonical structured source/fund snapshots | Authoritative for source data |
| `data/thesis.yaml` | Bottleneck control plane | Authoritative thesis state |
| `src/report.py` | Derived presentation | Not a source of new facts |

### Canonical Subflows

```
EARNINGS SUBFLOW

wiki/raw/<ticker>-<quarter>-*.md
  -> wiki/sources/<ticker>-<quarter>.md
  -> data/companies/<TICKER>/q*.yaml
  -> optional thesis.yaml update
```

```
13F / SOURCE SUBFLOW

wiki/raw/<fund>-<quarter>-13f.md
  -> wiki/sources/<fund>-<quarter>.md
  -> data/sources/<fund>/q*.yaml
  -> optional thesis.yaml update
```

```
CONCEPT SUBFLOW

new source/company evidence
  -> wiki/concepts/<topic>.md refresh
  -> no thesis.yaml change unless structured evidence changed state
```

## Agent Sidecar Pipeline

This lane exists to move faster, test automation, and generate learning signals without mutating canonical truth directly.

```
AGENT SIDECAR (non-authoritative)

reads wiki/raw when available + wiki/* + data/* + data/thesis.yaml
  -> agents/src/transcript_fetcher.py
     writes transcript drafts to agents/drafts/earnings/

  -> agents/src/earnings_calendar.py
     writes agents/reports/earnings-alert-YYYY-MM-DD.md

  -> agents/src/pre_earnings_predictor.py
     writes agents/state/predictions/<TICKER>-<quarter>.yaml

  -> agents/src/post_earnings_scorer.py
     writes agents/reports/scorecard-<TICKER>-<quarter>.md

  -> agents/src/report.py
     writes agents/reports/latest.html

  -> agents/autoagent/backtest.py
     writes agents/autoagent/experiments/*

  -> ad hoc daily briefings
     writes agents/reports/daily-YYYY-MM-DD.md
```

- Agents may read the full repo.
- Agents should write only under `agents/`.
- Agent outputs are proposals, comparisons, or scoring artifacts, not canonical truth.
- `agents/config.yaml` currently advertises a weekly `thirteenf_monitor` and daily `signal_scanner`, but those scripts do not exist yet.

## Promotion Gate

The only way information should move from the agent lane back into the canonical lane is through explicit human review.

```
AGENT OUTPUT / LOCAL RESEARCH
  -> human review
  -> if worth keeping:
     raw evidence      -> wiki/raw/
     event synthesis   -> wiki/sources/
     concept updates   -> wiki/concepts/
     structured facts  -> data/companies/ or data/sources/
     thesis state      -> data/thesis.yaml
```

Rule: agents can propose; the canonical lane decides.

## Alignment Contract

The repo has one truth path. `wiki/` and `data/` are not peers; they are adjacent layers in the same promotion funnel.

```
external evidence
  -> wiki/raw/                    immutable source artifact
  -> wiki/sources/                human-readable synthesis
  -> data/companies/ + data/sources/
                                  canonical structured facts / claims / positions
  -> data/thesis.yaml             control plane for bottlenecks, ticker map, dates
  -> src/synthesis.py + src/report.py
                                  derived views only
```

Enforcement lives at the handoffs, not inside ad hoc prose:

| Transition | Contract | Enforcement |
|---|---|---|
| `external -> wiki/raw/` | Raw artifact exists and is immutable after ingest | Missing raw files are drift findings |
| `wiki/raw/ -> wiki/sources/` | Source page must cite the raw or structured upstream artifact | Frontmatter `sources:` must resolve |
| `wiki/sources/ -> data/companies/` | Deep-dive earnings pages get a structured twin | Parity check: source page <-> company YAML |
| `data/companies/ -> data/thesis.yaml` | Thesis only changes when structured evidence changes status | Promotion gate: thesis updates are downstream-only |
| `data/* -> synthesis/report` | Report renders canonical state, not new truth | Drift and dashboard surfaces read from `data/*` |

Ownership is explicit:

| Layer | Owns | Must not own |
|---|---|---|
| `wiki/raw/` | source artifact | interpretation |
| `wiki/sources/` | narrative, quotes, context, wikilinks | canonical status or final machine-readable facts |
| `data/companies/` + `data/sources/` | financials, claim status, positioning, thesis signals | long-form prose |
| `data/thesis.yaml` | stage status, ticker map, catalyst dates | bulky evidence blobs |
| `src/synthesis.py` + `src/report.py` | derived views | new facts |

If the same fact appears in both wiki prose and structured data, `data/` wins. Wiki explains the thesis; `data/` remembers what is true.

## Raw Layer Notes

`wiki/raw/` is still the intended first stage of the canonical pipeline.

- It was **not** replaced by new terminology.
- It is **local-first and gitignored** because raw transcripts/filings can be large, regeneratable, or copyright-sensitive.
- A fresh checkout may have an empty or missing `wiki/raw/` directory until local ingest happens. That does not mean the architectural layer is gone.
- `agents/drafts/earnings/` is **not** a rename of `wiki/raw/`; it is an agent staging area.
- If a source page in `wiki/sources/` points to `raw/...`, that is still the intended canonical upstream evidence link.

## Current Operating Cadence

The live repo has both manual and agentic cadence, but only some of it is automated today.

| Cadence | Canonical manual/wiki path | Agent sidecar path |
|---|---|---|
| Morning / daily | Review news, daily notes, and decide what is worth ingesting into `wiki/raw/` / `wiki/sources/` | Daily briefings in `agents/reports/daily-*.md`; `agents/src/earnings_calendar.py` is the clearest implemented daily script |
| Weekly | Manual review of new 13Fs, source changes, open research gaps, and thesis drift | Intended weekly 13F monitor in config, but not implemented yet |
| Monthly | Manual cascade review, deep-dive backlog pruning, and thesis-control-plane cleanup | No implemented monthly agent review yet |
| Pre-earnings | Canonical prep: read prior raw/source/company material and score prior claims | `agents/src/pre_earnings_predictor.py` generates testable claims ~7 days before earnings |
| Post-earnings | Canonical raw -> source -> company update, then thesis update if needed | `agents/src/post_earnings_scorer.py` scores predictions and writes scorecards |
| Quarterly | Canonical 13F ingest and fund-positioning refresh | Backtests and predictor tuning can run in parallel via AutoAgent |

## Next Bottleneck: Narrowing

The next bottleneck is not more ingestion. It is better compression between the canonical data layers and the report surfaces.

```
PROPOSED COMPUTED MIDDLE LAYER

wiki/sources/*.md + data/companies/* + data/sources/* + data/thesis.yaml
  -> normalization adapters
     revenue | gross margin | EPS | cash flow | capex | guide | thesis signals | positioning

  -> derived metrics
     guide delta | margin acceleration | capex intensity | balance-sheet stress
     forward-claim status | thesis confirmation / weakening

  -> insight ranking
     what changed since last run
     which bottleneck got stronger / weaker
     which ticker has the most important new evidence
     which catalyst matters in the next 7-14 days

  -> report surfaces
     reports/latest.html
     agents/reports/earnings-alert-*.md
     future catalyst-first alerts
```

- **Normalization layer:** one adapter per tracked company so CRWV, NVDA, MU, TSM, INTC, COHR, and LITE expose the same comparison surface.
- **Derived-metrics layer:** computed signals the report actually reasons on, instead of every surface reparsing quarter YAML independently.
- **Insight layer:** ranking and compression, not storage.
- **Backfill requirement:** one more prior quarter for core names where the comparison materially sharpens the signal.
- **Anti-bloat rule:** do not create a third hand-maintained truth lane. This layer should be computed from canonical inputs.

## Proposed Reflection Cadence

Once the narrowing layer exists, the morning / weekly / monthly process can sit on top of it without bloating the repo.

```
PROPOSED CADENCE LAYER

daily briefing + earnings alert + insight ranking + thesis context
  -> agents/reports/reflections/daily-YYYY-MM-DD.md

5-7 daily reflections
  -> agents/reports/reflections/weekly-YYYY-MM-DD.md

4-5 weekly reflections + due claims + upcoming quarter schedule
  -> agents/reports/reflections/monthly-YYYY-MM-DD.md

weekly / monthly proposals
  -> human review
  -> promote only accepted changes into wiki/raw, wiki/sources, wiki/concepts,
     data/companies, data/sources, or data/thesis.yaml
```

## Source Cadence

- **13F filings:** quarterly, typically mid-February / mid-May / mid-August / mid-November
- **SemiAnalysis:** continuous manual curation into `data/sources/semianalysis/signals.yaml`
- **Earnings calls:** event-driven funnel through `wiki/raw/`, `wiki/sources/`, `data/companies/`, and sometimes `data/thesis.yaml`
 
