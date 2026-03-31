# semi-stocks

Investment research repo tracking AI infrastructure bottleneck rotation.

## Context

This project captures the thesis that AI compute demand is systematically underestimated by the semiconductor supply chain. We track three primary sources to identify which physical bottleneck is binding and where asymmetric returns exist.

## Sources

| Source | What they provide | How to access |
|--------|------------------|---------------|
| **SemiAnalysis** (Dylan Patel) | Supply chain data: wafer allocations, fab construction, tool shipments, DC tracking | [newsletter.semianalysis.com](https://newsletter.semianalysis.com) |
| **Leopold Aschenbrenner** (Situational Awareness LP) | High-conviction fund positioning, AGI timeline thesis | 13F via [WhaleWisdom](https://whalewisdom.com/filer/situational-awareness-lp) |
| **Gavin Baker** (Atreides Management) | Semiconductor supply chain positioning, public commentary | 13F via [WhaleWisdom](https://whalewisdom.com/filer/atreides-management-lp) |

## Key Concepts

- **Bottleneck cascade:** Constraints shift in sequence (CoWoS → power → memory → N3 logic → EUV tools). The money is in identifying the *next* one.
- **X minus 1:** Everyone in the supply chain builds one step below what's actually needed. The gap = the trade.
- **Demand destruction:** AI memory demand is crowding out consumer devices. DRAM price 3-4x → smartphone volumes halving → more DRAM freed for AI. Track this feedback loop.
- **13F lag:** Filings are 45 days stale. Use SemiAnalysis data to infer what positions *should* look like next quarter.

## Rules for Claude Sessions

<important if="analyzing a new 13F filing or position change">
Always compare against the prior quarter. Calculate: position size change (%), new entries, full exits. Flag when Leopold and Baker move in opposite directions on the same name — that's a thesis divergence signal.
</important>

<important if="evaluating a stock in this context">
Frame analysis around: (1) which bottleneck does this company sit on, (2) is that bottleneck currently binding or next-in-line, (3) is the position held by Leopold, Baker, or both, (4) what does SemiAnalysis data say about the supply/demand for this company's product.
</important>

<important if="researching supply chain data">
Use parallel subagents to pull: SemiAnalysis newsletter (public posts), WhaleWisdom 13F data, recent earnings transcripts for the relevant company. Synthesize after all return.
</important>

<important if="user asks about a specific sector">
Map it to the bottleneck cascade. Provide: current constraint status, key companies, who holds what (Leopold vs Baker), and SemiAnalysis signal if available.
</important>

## File Structure

```
README.md          ← Thesis, sources, positioning data, actionable framework
CLAUDE.md          ← This file. Session instructions.
```
