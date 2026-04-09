# semi-stocks
  
Investment research tracking AI infrastructure bottleneck rotation. Sources, thesis, and positioning data live in `data/`. Check `TODO.md` at session start for current priorities.

## Core Thesis

AI compute demand is systematically underestimated. Bottlenecks shift in sequence — the trade is identifying the next one before consensus. See `data/thesis.yaml` for current cascade status.

## Key Concepts

- **Bottleneck cascade:** Constraints shift in sequence (CoWoS → power → memory → N3 logic → EUV tools). The money is in identifying the *next* one.
- **X minus 1:** Everyone in the supply chain builds one step below what's actually needed. The gap = the trade.
- **Demand destruction:** AI memory demand is crowding out consumer devices. DRAM price 3-4x → smartphone volumes halving → more DRAM freed for AI.
- **13F lag:** Filings are 45 days stale. Use SemiAnalysis data to infer what positions *should* look like next quarter.

## Key Files

| File | What's there |
|---|---|
| `README.md` | Full thesis prose, source descriptions (Leopold/Baker/SemiAnalysis), divergence table, actionable framework |
| `data/thesis.yaml` | Cascade status, ticker-to-bottleneck map, signals |
| `data/sources/{leopold,baker}/` | 13F positioning YAML (quarterly) |
| `data/sources/semianalysis/` | Curated supply chain signals |
| `data/companies/<TICKER>/` | Earnings analysis, forward claims, thesis signals (deep-dive names only) |
| `data/research/earnings-pipeline.md` | Full ingestion process docs (earnings + 13F funnels, query traversal) |
| `data/research/13f-pipeline-design.md` | 13F automation design |
| `wiki/` | Semi-stocks wiki. Read `wiki/schema.md` before any wiki op. Update `wiki/index.md` and `wiki/log.md` after changes. |
| `config.yaml` | Source URLs, CIKs |
| `src/synthesis.py` | Agreement map, divergences, cascade status |
| `src/report.py` | HTML report generator |

## Runtime Routing

<important if="touching the semi-stocks wiki, ingesting a source, or answering a wiki query">
Treat `wiki/` in the current repo as the only writable wiki root. Do not write to `/Users/ash/Documents/2026/wiki` or `/Users/ash/Documents/2026/semi-stocks/wiki` from this workspace.
Prefer `/ingest-semi` over the generic `/wiki` flow for semi-stocks wiki ingest, query, and lint work.
After wiki writes, update `wiki/index.md`, run `python3 ~/.dot-agent/skills/wiki/scripts/rebuild_index.py wiki`, and append `wiki/log.md`.
</important>

## Session Rules

<important if="analyzing a new 13F filing or position change">
Read `data/research/earnings-pipeline.md` § "13F funnel" for the full process. Route through wiki. Compare QoQ. Flag when Leopold and Baker move opposite directions on same name — that's a thesis divergence signal.
</important>

<important if="ingesting earnings or a transcript">
Read `data/research/earnings-pipeline.md` for the full process. Route through wiki funnel: `wiki/raw/` → `wiki/sources/` → `data/companies/`. Score prior `forward_claims` before ingesting new quarter. Deep-dive list: CRWV, NVDA, MU, COHR, INTC, TSM, LITE.
</important>

<important if="evaluating a stock in this context">
Frame analysis around: (1) which bottleneck does this company sit on, (2) is that bottleneck currently binding or next-in-line, (3) is the position held by Leopold, Baker, or both, (4) what does SemiAnalysis data say about the supply/demand for this company's product, (5) check `data/companies/` for earnings history and open forward claims.
</important>

<important if="researching supply chain data">
Use parallel subagents to pull: SemiAnalysis newsletter (public posts), WhaleWisdom 13F data, recent earnings transcripts for the relevant company. Synthesize after all return.
</important>

<important if="user asks about a specific sector">
Map it to the bottleneck cascade. Provide: current constraint status, key companies, who holds what (Leopold vs Baker), and SemiAnalysis signal if available.
</important>
