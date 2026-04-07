# Earnings Pipeline — Process Documentation

Date: 2026-04-07

All sources flow through the wiki funnel: raw → synthesized → structured. Two input streams feed the report:

```
                                  COLLECT       SYNTHESIZE       STRUCTURE         ACT
                                  (wide)                                          (narrow)

  Earnings/transcripts:           wiki/raw/  →  wiki/sources/  →  data/companies/  ─┐
                                                                                     ├→ synthesis.py → report
  13F fund positioning:           wiki/raw/  →  wiki/sources/  →  data/sources/    ─┤
                                                                                     │
  SemiAnalysis signals:           (manual curation)            →  data/sources/    ─┤
                                                                                     │
  Cascade / ticker map:                                           data/thesis.yaml ─┘
```

## Earnings funnel

Layered — wide at ingest, narrow at thesis:

| Layer | Location | Scope | Content |
|---|---|---|---|
| **Raw** | `wiki/raw/<ticker>-<quarter>-transcript.md` | ~20 companies | Full transcript, immutable after filing |
| **Synthesize** | `wiki/sources/<ticker>-<quarter>.md` | ~12-15 companies | Key metrics table, management quotes, guidance claims, wikilinks, cross-repo links to `data/companies/` |
| **Structure** | `data/companies/<TICKER>/q4_2025.yaml` | ~5-8 companies | Financials, `forward_claims:` with `verify_at:` dates and `status: pending|confirmed|missed|revised`, `thesis_signals:`, `positioning:` cross-ref |
| **Thesis** | `data/thesis.yaml` | Only when status shifts | Cascade status change, referencing the company/quarter that triggered it |

- Deep-dive list: CRWV, NVDA, MU, COHR, INTC, TSM, LITE
- Each new quarter: first step is scoring prior `forward_claims` where `verify_at` matches.
- Company deep dive template: see `data/research/13f-pipeline-design.md` § "Company Deep Dive Template"

## 13F funnel

When the user shares a new 13F:

1. Parallel subagents fetch + cross-check against SEC EDGAR + at least 2 aggregators
2. Store raw filing data in `wiki/raw/<fund>-<quarter>-13f.md`
3. Create/update `wiki/sources/<fund>-<quarter>.md` with QoQ diff and thesis signals
4. Diff against prior quarter in `data/sources/<name>/`
5. Present cross-checked tables — user approves before committing
6. Write YAML to `data/sources/`, update `data/thesis.yaml` if cascade changed
7. Log to `wiki/log.md` and `data/updates/YYYY-MM-DD.md`

## Query traversal

- Wiki queries start at `wiki/index.md`, read source pages, follow wikilinks.
- When a query needs structured data (QoQ comparison, claim verification, positioning), follow cross-repo links into `data/`.
- Wiki source pages are self-contained for most queries; structured data is the depth layer.

## Forward claims

Each `data/companies/<TICKER>/` YAML has a `forward_claims:` section:

```yaml
forward_claims:
  - claim: "Q1 margins will trough at low single digits"
    speaker: "CFO Nitin Agrawal"
    source: "Q4 2025 earnings call"
    verify_at: "Q1 2026 earnings"
    status: pending  # pending → confirmed | missed | revised
```

Next quarter, first step is: pull prior `forward_claims` with matching `verify_at` and score them. This builds a credibility track record per company over time.
