---
title: Research Control Plane
tags: [workflow, research, expectations, telemetry, risk]
sources: [sources/semi-stocks-repository-review-2026-04-09.md, ../data/thesis.yaml]
created: 2026-04-09
updated: 2026-04-09
---

# Research Control Plane

The bottleneck thesis is necessary but not sufficient. A serious rotation system also needs a control plane that answers three questions continuously:

1. What does the market already expect?
2. What is happening in the real world right now?
3. How much risk can the portfolio take while waiting for the thesis to play out?

## Expectations Layer

This layer tracks the market's current model:
- consensus estimates and revision velocity
- price, volume, volatility, and reactions versus expectations
- ownership breadth, crowding, and flow pressure
- where current positioning already reflects the thesis

Without this layer, the repo can identify a real bottleneck and still lose money by buying what is already consensus.

## Telemetry Layer

This layer tracks the physical state of the constraint:
- semiconductor indicators such as pricing, utilization, wafer shipments, and company-reported demand
- supply-chain relationship maps that show customer-supplier propagation
- non-chip physical indicators such as grid load growth, interconnection queues, delivered data-center megawatts, vacancy, and transformer/substation constraints

Without this layer, the thesis is too dependent on narrative synthesis rather than independent confirmation.

## Portfolio / Risk Layer

This layer translates the thesis into durable exposures:
- factor and beta exposure decomposition
- scenario libraries tied to each cascade stage
- liquidity-aware sizing and event-risk limits
- borrow, short-interest, and options-positioning checks where relevant

Without this layer, a portfolio can look diversified by ticker while still being one concentrated AI-risk trade.

## Workflow Cadence

Institutional process also requires repeatable operating loops:
- pre-earnings setup memos with market expectations and asymmetric risks
- post-earnings diffs that update claims, expectations, and stage status
- between-quarter calendars for recurring indicators
- postmortems that score prior calls against outcomes

The current repo already has the beginnings of this in `data/companies/`, `data/thesis.yaml`, and the forward-claims system. The missing piece is systematization across names and time.

## Relationship To The Existing Thesis

[[concepts/bottleneck-cascade]] answers where scarcity sits in the stack. The control plane answers whether that scarcity is priced, whether it is independently confirmed, and how aggressively it should be expressed.

That makes this page a meta-layer over:
- [[concepts/bottleneck-cascade]]
- [[concepts/power]]
- [[concepts/memory-supercycle]]
- [[concepts/n3-wafer-crunch]]
- [[concepts/pluggable-optics]]

See also: [[sources/semi-stocks-repository-review-2026-04-09]], [[outputs/baker-cyclicality-thesis]], [[concepts/bottleneck-cascade]], [[concepts/power]]
