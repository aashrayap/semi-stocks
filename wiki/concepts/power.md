---
title: Power / DC Buildout
tags: [power, data-centers, infrastructure, bottleneck]
sources: [../data/thesis.yaml, ../data/sources/leopold/q4_2025.yaml, ../data/companies/CRWV/q4_2025.yaml, sources/semi-stocks-repository-review-2026-04-09.md]
created: 2026-04-08
updated: 2026-04-09
---

# Power / DC Buildout

Power is the physical prerequisite for every AI factory. GPUs, racks, optics, and cooling do not matter if grid access, land, and interconnects are unavailable.

## Why It Was a Bottleneck

- AI data centers require utility-scale power and cooling, not normal colocation footprints
- PJM backlog remained 286 GW even after a wave of announced buildouts
- `data/thesis.yaml` tracks 56 GW of announced capacity, enough to move this stage from acute shortage to post-peak
- Bitcoin miners and power developers matter because they already control sites, interconnects, and cooling pathways

## Current Read

This stage is `played_out` in the market and `post_peak` in the thesis tracker, but not irrelevant. Power is no longer the cleanest scarcity trade; it is now the deployment substrate under GPU cloud and AI factory expansion.

## Source Positioning

- **Leopold:** still heavily positioned in power names and miners (BE, CORZ, IREN, EQT, and others)
- **Baker:** does not use power as the primary bottleneck expression
- **CRWV earnings:** 850+ MW active and 3.1+ GW contracted show the scale needed just to keep up

## Relationship to GPU Cloud

[[concepts/gpu-cloud]] is the revenue layer; power is the physical layer underneath it. GPU cloud demand can remain strong even as the pure-play power trade becomes more consensus and less asymmetric.

## Telemetry To Watch

The repository review sharpened one important point: power should not be tracked only through equity narratives or SemiAnalysis summaries. A durable power view needs direct telemetry such as:

- grid and utility load forecasts
- interconnection queues and permit timing
- delivered data-center megawatts, vacancy, and under-construction capacity
- transformer, substation, and other electrical-equipment lead times

This is the clearest stage where the repo needs [[concepts/research-control-plane|research control plane]] discipline around physical-world data.

See also: [[concepts/bottleneck-cascade]], [[concepts/gpu-cloud]], [[concepts/research-control-plane]], [[sources/leopold-q4-2025]], [[sources/crwv-q4-2025]], [[sources/semi-stocks-repository-review-2026-04-09]]
