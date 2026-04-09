---
title: Copper Signal Integrity
tags: [copper, retimers, signal-integrity, networking]
sources: [../data/thesis.yaml, ../data/sources/baker/q4_2025.yaml]
created: 2026-04-08
updated: 2026-04-08
---

# Copper Signal Integrity

Copper still dominates inside the rack even while optical links win between racks. That creates a distinct bottleneck for retimers, redrivers, and signal-integrity components at higher lane speeds.

## Why It Matters

- `data/thesis.yaml` explicitly keeps copper inside the rack through NVL1152 in the base case
- 200G per lane and 448G SerDes push reach, power, and signal quality hard enough that copper still needs specialized conditioning
- This is why the repo tracks ALAB and SMTC separately from pure optical names

## Current Read

This is an adjacency to [[concepts/pluggable-optics]] and [[concepts/co-packaged-optics]], not a replacement for them. If CPO adoption stays slower than the hype cycle suggests, copper signal-integrity names get a longer runway.

## Source Positioning

| Ticker | Role | Baker |
|--------|------|-------|
| ALAB | PCIe/CXL retimers and connectivity silicon | $268M |
| SMTC | Signal-integrity ICs | $51M |

Baker is the main explicit owner here. Leopold's optical expression is concentrated in COHR and LITE instead.

See also: [[concepts/pluggable-optics]], [[concepts/co-packaged-optics]], [[sources/baker-q4-2025]]

