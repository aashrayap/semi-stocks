# ash.md

Human briefing for `semi-stocks`. This is a short mental model for reading and iterating on the repo. It is not canonical truth and not an agent instruction file.

## Repo In One Picture

```text
REAL WORLD
  earnings / 13Fs / supply-chain notes / articles
      |
      v
CAPTURE
  wiki/raw/                  immutable evidence
      |
      v
EXPLAIN
  wiki/sources/              event writeups
  wiki/concepts/             cross-cutting thesis pages
      |
      v
REMEMBER
  data/companies/            quarter facts and forward-claim scoring
  data/sources/              fund and source snapshots
  data/thesis.yaml           current bottleneck map
      |
      v
COMPARE / ACT
  reports/latest.html
  next catalyst to ingest
  next thesis state to test
```

## What This Repo Is Trying To Do

- Track where the AI infrastructure bottleneck sits before consensus does.
- Convert messy evidence into a small canonical control plane.
- Improve the system incrementally so each quarter is easier to compare than the last.

## Read In This Order

1. `README.md`
2. `data/thesis.yaml`
3. `wiki/concepts/bottleneck-cascade.md`
4. `wiki/concepts/source-triangulation.md`
5. `TODO.md`

## How To Iterate

| If you are learning about... | Update first | Promote to | Why |
|---|---|---|---|
| Earnings | `wiki/raw/` + `wiki/sources/` | `data/companies/` | Keeps quarter metrics and forward claims comparable |
| 13F / fund moves | `wiki/raw/` + `wiki/sources/` | `data/sources/` | Makes positioning shifts explicit |
| Cross-cutting thesis change | `wiki/concepts/` | `data/thesis.yaml` if status changed | Avoids jumping straight from idea to control plane |
| Workflow gap | `TODO.md` or a concept page | later automation | Keeps process changes visible before coding them |

## Good Next Improvements

- Automate 13F ingest from EDGAR and strip options cleanly.
- Build a normalization layer so tracked companies compare cleanly across quarters.
- Add expectation and risk overlays, not just physical bottleneck telemetry.
- Tighten catalyst prep around the next 7-14 days, not just historical ingest.

## Rule Of Thumb

Use `wiki/` to explain, `data/` to remember what is true, and reports to compress what changed.
