# agents/ — Agent Fleet Workspace

You are an automated agent operating in the semi-stocks research repo. This file defines your permissions and operating rules.

## Boundary Rules

- **FULL READ access** to every file in the semi-stocks repo (data/, wiki/, src/, config.yaml, etc.)
- **WRITE ONLY to agents/** — you may not create or modify files outside this directory
- This boundary is absolute. No exceptions.

## Key Files to Read

| File | Why |
|---|---|
| `data/thesis.yaml` | Bottleneck cascade status, ticker map, next_earnings dates, signals |
| `data/research/earnings-pipeline.md` | Full earnings + 13F ingestion process |
| `data/research/13f-pipeline-design.md` | 13F automation design |
| `config.yaml` | Source URLs, CIKs, deep_dive ticker list |
| `data/companies/<TICKER>/` | Quarterly earnings YAML with forward_claims, thesis_signals, positioning |
| `data/sources/leopold/` | Leopold 13F positioning (quarterly) |
| `data/sources/baker/` | Baker 13F positioning (quarterly) |
| `data/sources/semianalysis/` | Curated supply chain signals |
| `wiki/schema.md` | Wiki conventions — read before any wiki reads |
| `wiki/index.md` | Wiki page catalog — start queries here |
| `wiki/sources/` | Synthesized earnings/13F pages |
| `wiki/concepts/` | Compiled knowledge articles (bottleneck-cascade, memory-supercycle, etc.) |
| `src/synthesis.py` | Agreement map, divergences, cascade logic |
| `src/report.py` | HTML report generator (reference for output format) |

## Output Locations

| Directory | Purpose |
|---|---|
| `agents/reports/` | Agent-generated reports (HTML, Markdown). Parallel to main `reports/`. |
| `agents/drafts/13f/` | Draft 13F analysis awaiting human review |
| `agents/drafts/earnings/` | Draft earnings analysis awaiting human review |
| `agents/drafts/signals/` | Draft signal alerts awaiting human review |
| `agents/logs/` | Run logs — always log when you execute |
| `agents/state/` | Tracking state (last poll times, processed filings, etc.) |

## Prediction Eval Loop

The agent fleet runs a prediction-scoring loop around every earnings call:

1. **Pre-earnings (7 days before):** `pre_earnings_predictor.py` reads the entire knowledge graph (thesis, company data, fund positioning, SemiAnalysis signals, wiki concepts) and generates deterministic, testable predictions. Output: `agents/state/predictions/<TICKER>-<quarter>.yaml`. These are template-based drafts — a human or agent refines them before earnings.

2. **Post-earnings:** `post_earnings_scorer.py` grades each prediction against actual results. Use `--interactive` for human-assisted scoring (prints each claim, prompts for confirmed/missed/partial/revised). Without `--interactive`, it generates a template scorecard for later manual review. Updates the predictions YAML in-place and writes a scorecard to `agents/reports/scorecard-<TICKER>-<quarter>.md`.

3. **Meta (ongoing):** Over time, the track record accumulates across quarters. The scorer tracks:
   - Overall accuracy per ticker
   - Accuracy by prediction category (capacity, pricing, demand, margins, guidance, positioning)
   - Which basis sources (thesis.yaml, SemiAnalysis, wiki, company data, fund positioning) produce correct vs. incorrect predictions
   - Historical accuracy trend per ticker

This loop makes the research system self-correcting: if capacity predictions are always right but guidance predictions always miss, the system learns which categories and sources to trust.

## Operating Rules

1. **Drafts are proposals.** Files in `agents/drafts/` are suggestions. A human reviews and decides whether to promote content to the main `data/` or `wiki/` directories.
2. **Reports run parallel.** Agent reports in `agents/reports/` exist for comparison against human-curated main reports. They do not replace them.
3. **Always log runs.** Every agent execution must append to `agents/logs/`. Include: timestamp, agent name, tickers processed, files read, files written, errors.
4. **Self-contained execution.** Agent scripts in `agents/src/` must not import from `src/`. They read YAML/Markdown files directly. Dependencies: pyyaml, pathlib (stdlib).
5. **Use pathlib.** All paths resolve relative to the script's location, walking up to repo root.
6. **Respect the funnel.** The research pipeline is: raw -> synthesized -> structured -> thesis. Read `data/research/earnings-pipeline.md` to understand layering. Agent outputs should follow the same structure.
7. **Config-driven.** Read `agents/config.yaml` for polling intervals, tracked tickers, and alert thresholds.
