# agents/ — Automated Agent Fleet

Automated agents that monitor the semi-stocks research repo and produce parallel reports, alerts, and draft analyses for human review.

## What This Is

The main semi-stocks repo contains human-curated investment research: thesis tracking, earnings analysis, 13F fund positioning, and supply chain signals. The `agents/` directory is a sandboxed workspace where automated agents can read all of that data and produce their own outputs — without modifying the curated research.

## Boundary Rules

| Access | Scope |
|---|---|
| **Read** | Everything in the repo: `data/`, `wiki/`, `src/`, `config.yaml`, `README.md`, etc. |
| **Write** | `agents/` only. Agents cannot create or modify files outside this directory. |

## Relationship to Main Repo

- Agent reports in `agents/reports/` run parallel to human reports in `reports/`. Compare them to catch drift or missed signals.
- Agent drafts in `agents/drafts/` are proposals. A human reviews before promoting content to `data/` or `wiki/`.
- Agents read `data/thesis.yaml` and `config.yaml` as their source of truth for what to track.

## Structure

```
agents/
  CLAUDE.md              -- Instructions for agents operating here
  README.md              -- This file
  config.yaml            -- Agent fleet config (tickers, intervals, thresholds)
  src/
    earnings_calendar.py -- Earnings alert agent
    pre_earnings_predictor.py -- Pre-earnings prediction generator
    post_earnings_scorer.py   -- Post-earnings prediction scorer
  reports/               -- Agent-generated reports + scorecards
  drafts/
    13f/                 -- Draft 13F analyses
    earnings/            -- Draft earnings analyses
    signals/             -- Draft signal alerts
  logs/                  -- Agent run logs
  state/
    predictions/         -- Prediction YAMLs per ticker per quarter
```

## Agents

### earnings_calendar.py

Scans `data/thesis.yaml` for upcoming earnings dates, cross-references `data/companies/` for pending forward claims, pulls context from `wiki/sources/`, and outputs a structured alert to `agents/reports/`.

```bash
python agents/src/earnings_calendar.py
python agents/src/earnings_calendar.py --days 21
```

Output: `agents/reports/earnings-alert-YYYY-MM-DD.md`

### pre_earnings_predictor.py

The most important agent. Before each earnings call, reads the entire knowledge graph and generates testable predictions. Predictions are deterministic templates filled from data — no LLM. A human or agent refines afterward.

```bash
# Single ticker
python agents/src/pre_earnings_predictor.py --ticker TSM --quarter Q1_2026

# All tickers with earnings in next 7 days
python agents/src/pre_earnings_predictor.py --all-upcoming

# Preview without writing
python agents/src/pre_earnings_predictor.py --ticker TSM --quarter Q1_2026 --dry-run
```

Output: `agents/state/predictions/<TICKER>-<quarter>.yaml`

### post_earnings_scorer.py

After earnings, scores predictions against what happened. Supports interactive human-assisted scoring or template generation for later review.

```bash
# Interactive scoring (prompts for each prediction)
python agents/src/post_earnings_scorer.py --ticker TSM --quarter Q1_2026 --interactive

# Template scorecard for manual review
python agents/src/post_earnings_scorer.py --ticker TSM --quarter Q1_2026

# Preview without writing
python agents/src/post_earnings_scorer.py --ticker TSM --quarter Q1_2026 --dry-run
```

Output:
- Updates `agents/state/predictions/<TICKER>-<quarter>.yaml` (status changes)
- Writes `agents/reports/scorecard-<TICKER>-<quarter>.md`

## Prediction Eval Loop

1. **Pre-earnings (7 days out):** predictor generates testable claims from the knowledge graph
2. **Post-earnings:** scorer grades predictions, updates track record
3. **Meta:** over time, track which bottleneck categories and source types produce accurate predictions

## Adding New Agents

1. Add the script to `agents/src/`
2. Add any config to `agents/config.yaml`
3. Follow the rules in `agents/CLAUDE.md`: read anything, write only to `agents/`, always log, self-contained execution
