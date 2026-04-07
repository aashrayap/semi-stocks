# Wiki Schema — semi-stocks

Rules and conventions for the semi-stocks investment research wiki. Co-evolved by Ash and Claude.

## Directory structure

```
semi-stocks/wiki/
├── index.md          ← master catalog of all pages (LLM-maintained)
├── log.md            ← append-only activity log
├── schema.md         ← this file — conventions and workflows
├── raw/              ← immutable source documents (transcripts, articles, 13F snapshots)
│   └── assets/       ← downloaded images
├── concepts/         ← compiled knowledge articles (LLM-written)
├── sources/          ← per-source summary pages (LLM-written)
└── outputs/          ← filed query results, analysis
```

## Three layers

1. **Raw sources** (`raw/`) — immutable. LLM reads but never modifies.
2. **The wiki** (`concepts/`, `sources/`, `outputs/`) — LLM-owned. LLM creates, updates, cross-references. Human reads but rarely edits.
3. **The schema** (this file) — co-evolved. Defines conventions, workflows, page formats.

## Thesis link

This wiki is linked to the semi-stocks data layer:

```yaml
thesis_link: ../data/thesis.yaml
data_sources: ../data/sources/
```

During ingest, the LLM checks whether new sources contain thesis-relevant data (signals, status changes, new tickers, positions) and proposes YAML patches. See the wiki skill for the full thesis patch workflow.

## Page format

Every wiki page uses this frontmatter:

```yaml
---
title: Page Title
tags: [tag1, tag2]
sources: [raw/filename.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body is markdown with:
- Wikilinks for cross-references: `[[concepts/bottleneck-cascade]]`
- Section headers for scanability
- "See also" section at bottom linking related pages

## Cross-repo links

Wiki pages can reference the parent wiki and other 2026 repos:
- `[[wiki/concepts/ai-landscape]]` — parent wiki concept
- `[[semi-stocks/data/thesis.yaml]]` — thesis data

## Cross-repo query traversal

Wiki queries start at `index.md` and follow wikilinks through `concepts/` and `sources/`. When a query needs structured data — QoQ financials, claim verification, fund positioning — follow cross-repo links into `semi-stocks/data/`.

```
wiki/index.md  →  wiki/sources/<ticker>-<quarter>.md  →  data/companies/<TICKER>/q<N>_<year>.yaml
                  wiki/concepts/<topic>.md             →  data/thesis.yaml
                                                       →  data/sources/<fund>/q<N>_<year>.yaml
```

**Principle:** Wiki source pages should be self-contained for most queries. They have prose summary, key metrics, guidance claims. `data/` is the depth layer — only traverse there when queries need structured comparison, claim status, or positioning cross-reference.

Each earnings source page includes a `## Semi-stocks data` section at the bottom with explicit links to the structured data.

## Earnings source page template

For `sources/<ticker>-<quarter>.md` pages created from earnings calls:

```markdown
---
title: "<Company> — <Quarter> Earnings"
tags: [earnings, <ticker>, <bottleneck-tag>]
sources: [raw/<ticker>-<quarter>-transcript.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Company> — <Quarter> Earnings

<1-2 sentence summary: what happened, market reaction>

## Key Metrics

| Metric | Value | QoQ | YoY |
|--------|-------|-----|-----|
| Revenue | | | |
| Adj. EBITDA | | | |
| Gross Margin | | | |
| CapEx | | | |
| Backlog | | | |
| Debt | | | |

## Guidance

<Forward targets with consensus comparison>

## Forward Claims

Verifiable statements management made. These get tracked in `data/companies/` YAML.

- "<exact quote or paraphrase>" — <speaker>, verify at <quarter>
- ...

## Notable Quotes

<2-4 quotes tagged by topic: demand, pricing, capacity, competition>

## Thesis Signal

Which bottleneck does this confirm or contradict? Link to [[concepts/]] pages.

## Semi-stocks data

Structured data: `data/companies/<TICKER>/q<N>_<year>.yaml`
Fund positioning: `data/sources/leopold/`, `data/sources/baker/`
Cascade status: `data/thesis.yaml`

See also: [[relevant concept and source pages]]
```

## Naming conventions

- Filenames: lowercase, hyphenated (`bottleneck-cascade.md`)
- One concept per page
- Prefer specific pages over mega-pages
