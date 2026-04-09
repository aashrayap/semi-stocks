# TODO

## Now
- [ ] Test /report skill end-to-end

## Next
- [ ] 13F pipeline upgrade — automated EDGAR ingestion with options stripping
      See: `data/research/13f-pipeline-design.md`
      Refs: github.com/martinshkreli/13F, edgartools (PyPI)
- [ ] Work next tracked catalysts with the hardened pipeline (ASML 2026-04-15, TSM 2026-04-16, INTC 2026-04-23)
- [ ] Earnings calendar in config.yaml for proactive prompting
- [ ] Scheduled agent for source change detection
- [ ] "Who else is buying?" scanner — bulk 13F scan for thesis tickers

## Done
- [x] Complete COHR as second full-pipeline example (only full agreement zone across all 3 sources)
- [x] Complete remaining deep-dive watchlist coverage (MU, INTC, TSM, LITE)
- [x] Wire `data/companies/` into `synthesis.py` — forward claims, thesis signals, earnings financials as new report inputs
- [x] First live ingestion — CRWV Q4 2025 earnings (full pipeline: raw → wiki source → data/companies/)
- [x] Document earnings pipeline (extracted to `data/research/earnings-pipeline.md`)
- [x] Progressive disclosure rewrite of CLAUDE.md (conditional blocks, thin router)
- [x] Semi-stocks wiki scaffolded with concept + source pages
- [x] Cross-repo traversal documented in wiki/schema.md

## Someday
- [ ] Port predictions engine from trader_bot_v2 (thesis-tagged)
- [ ] Marimo notebook as interactive report surface
- [ ] Expand beyond semis (Valley Forge Capital, other superinvestors)
