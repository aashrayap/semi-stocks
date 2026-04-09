"""Synthesis engine — cross-source agreement, divergence, and thesis mapping."""

import re
import yaml
from pathlib import Path

from src.sources.base import DATA_DIR
from src.sources.fund_13f import Fund13FSource
from src.sources.semianalysis import SemiAnalysisSource

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
WIKI_RAW_DIR = WIKI_DIR / "raw"
WIKI_SOURCES_DIR = WIKI_DIR / "sources"
WIKI_CONCEPTS_DIR = WIKI_DIR / "concepts"
COMPANIES_DIR = DATA_DIR / "companies"

# Map cascade stage names to concept page filenames
STAGE_TO_CONCEPT = {
    "Memory supercycle": "memory-supercycle",
    "N3 logic wafers": "n3-wafer-crunch",
    "Pluggable optics (scale-out)": "pluggable-optics",
    "Co-packaged optics / CPO (scale-up)": "co-packaged-optics",
}

# Deep-dive names expected to move through the full earnings funnel.
DEEP_DIVE_TICKERS = {"CRWV", "NVDA", "MU", "COHR", "INTC", "TSM", "LITE"}

# Map ticker-level bottlenecks to the concept pages that explain them.
BOTTLENECK_TO_CONCEPT = {
    "memory": "memory-supercycle",
    "n3_logic": "n3-wafer-crunch",
    "pluggable_optics": "pluggable-optics",
    "cpo_next": "co-packaged-optics",
    "gpu_cloud": "gpu-cloud",
    "power": "power",
    "copper_signal_integrity": "copper-signal-integrity",
    "euv": "euv-tools",
    "foundry": "foundry",
}


def load_thesis() -> dict:
    """Load the thesis/cascade definition."""
    path = DATA_DIR / "thesis.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def get_sources() -> tuple[Fund13FSource, Fund13FSource, SemiAnalysisSource]:
    """Return all active sources."""
    leopold = Fund13FSource("leopold")
    baker = Fund13FSource("baker")
    semi = SemiAnalysisSource()
    return leopold, baker, semi


def _load_frontmatter(path: Path) -> dict:
    """Read YAML frontmatter from a markdown page."""
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def _quarter_to_slug(quarter: str) -> str:
    """Convert a quarter label like 'Q4 FY2026' into a filename slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", quarter.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def _company_source_slug(company: dict) -> str:
    """Return the expected wiki source slug for a company quarter."""
    ticker = str(company.get("ticker", "")).lower().strip()
    quarter = _quarter_to_slug(str(company.get("quarter", "")))
    return f"{ticker}-{quarter}".strip("-")


def _expected_company_yaml_from_source_slug(slug: str) -> str:
    """Infer the expected company YAML path from an earnings source slug."""
    ticker, _, quarter_slug = slug.partition("-")
    quarter_part = quarter_slug.replace("-", "_")
    return f"data/companies/{ticker.upper()}/{quarter_part}.yaml"


def _expected_source_page_from_company(company: dict) -> str:
    """Infer the expected wiki source page path from a company quarter."""
    return f"wiki/sources/{_company_source_slug(company)}.md"


def all_tickers() -> list[str]:
    """Return deduplicated list of all tickers across all sources."""
    leopold, baker, semi = get_sources()
    seen = []
    for t in leopold.tickers() + baker.tickers() + semi.tickers():
        if t not in seen:
            seen.append(t)
    return seen


def ticker_briefing(ticker: str) -> dict:
    """Build a cross-source briefing for a single ticker."""
    leopold, baker, semi = get_sources()
    thesis = load_thesis()

    ticker_meta = thesis.get("ticker_map", {}).get(ticker, {})

    return {
        "ticker": ticker,
        "bottleneck": ticker_meta.get("bottleneck"),
        "bottleneck_status": ticker_meta.get("status"),
        "leopold": leopold.lookup(ticker),
        "baker": baker.lookup(ticker),
        "semianalysis": semi.lookup(ticker),
    }


def agreement_map() -> list[dict]:
    """Build the source agreement/divergence map for all thesis-relevant tickers."""
    leopold, baker, semi = get_sources()
    thesis = load_thesis()
    ticker_map = thesis.get("ticker_map", {})

    results = []
    for ticker in ticker_map:
        l = leopold.lookup(ticker)
        b = baker.lookup(ticker)
        s = semi.lookup(ticker)

        held_by = []
        if l:
            held_by.append("leopold")
        if b:
            held_by.append("baker")
        if s:
            held_by.append("semianalysis")

        if not held_by:
            continue

        # Classify agreement level
        if len(held_by) == 3:
            agreement = "full"
        elif len(held_by) == 2:
            agreement = "partial"
        else:
            agreement = "single"

        results.append({
            "ticker": ticker,
            "bottleneck": ticker_map[ticker].get("bottleneck"),
            "status": ticker_map[ticker].get("status"),
            "held_by": held_by,
            "agreement": agreement,
            "leopold_value": l["value"] if l and "value" in l else None,
            "leopold_pct": l["pct_portfolio"] if l and "pct_portfolio" in l else None,
            "baker_value": b["value"] if b and "value" in b else None,
            "baker_pct": b["pct_portfolio"] if b and "pct_portfolio" in b else None,
            "semi_signals": len(s["signals"]) if s and "signals" in s else 0,
            "next_earnings": ticker_map[ticker].get("next_earnings"),
        })

    # Sort: full agreement first, then by total value
    results.sort(key=lambda r: (
        -{"full": 3, "partial": 2, "single": 1}[r["agreement"]],
        -(r["leopold_value"] or 0) - (r["baker_value"] or 0),
    ))
    return results


def divergences() -> list[dict]:
    """Find tickers where Leopold and Baker are positioned in opposite directions."""
    leopold, baker, _ = get_sources()

    divs = []

    # Check tickers held by one but not the other (among thesis-relevant names)
    thesis = load_thesis()
    ticker_map = thesis.get("ticker_map", {})

    for ticker in ticker_map:
        l = leopold.lookup(ticker)
        b = baker.lookup(ticker)

        if l and not b:
            divs.append({
                "ticker": ticker,
                "type": "leopold_only",
                "leopold_value": l.get("value"),
                "leopold_pct": l.get("pct_portfolio"),
                "notes": l.get("notes"),
            })
        elif b and not l:
            divs.append({
                "ticker": ticker,
                "type": "baker_only",
                "baker_value": b.get("value"),
                "baker_pct": b.get("pct_portfolio"),
                "notes": b.get("notes"),
            })
        elif l and b:
            # Both hold — check for directional disagreement (long vs put)
            l_type = l.get("type", "common")
            b_type = b.get("type", "common")
            if l_type == "put" and b_type != "put":
                divs.append({
                    "ticker": ticker,
                    "type": "directional",
                    "leopold": f"{l_type} ${l.get('value', 0):,}",
                    "baker": f"{b_type} ${b.get('value', 0):,}",
                })
            elif b_type == "put" and l_type != "put":
                divs.append({
                    "ticker": ticker,
                    "type": "directional",
                    "leopold": f"{l_type} ${l.get('value', 0):,}",
                    "baker": f"{b_type} ${b.get('value', 0):,}",
                })

    return divs


def cycle_assessment() -> list[dict]:
    """Generate Baker-framework cycle risk assessment per cascade stage.

    Reads cycle_phase, cycle_signal, and cycle_risk_flags from thesis.yaml
    and returns a structured assessment for each stage.
    """
    thesis = load_thesis()
    cascade = thesis.get("cascade", [])

    PHASE_META = {
        "resolved":       {"label": "Resolved",       "action": "—",           "risk": 0},
        "post_peak":      {"label": "Post-Peak",      "action": "Avoid",       "risk": 1},
        "peak_shortage":  {"label": "Peak Shortage",   "action": "Long + Puts", "risk": 3},
        "mid_shortage":   {"label": "Mid Shortage",    "action": "Long + Hedge","risk": 2},
        "early_cycle":    {"label": "Early Cycle",     "action": "Long",        "risk": 1},
        "pre_cycle":      {"label": "Pre-Cycle",       "action": "Watch",       "risk": 0},
    }

    results = []
    for stage in cascade:
        phase = stage.get("cycle_phase", "")
        meta = PHASE_META.get(phase, {"label": phase, "action": "?", "risk": 0})
        results.append({
            "name": stage["name"],
            "status": stage["status"],
            "cycle_phase": phase,
            "cycle_label": meta["label"],
            "cycle_action": meta["action"],
            "cycle_risk": meta["risk"],
            "cycle_signal": stage.get("cycle_signal", ""),
            "cycle_risk_flags": stage.get("cycle_risk_flags", []),
            "tickers": stage.get("tickers", []),
            "period": stage.get("period", ""),
        })

    return results


def baker_hedge_ratio() -> dict:
    """Return Baker's current hedge ratio and trend from thesis.yaml."""
    thesis = load_thesis()
    data = thesis.get("baker_hedge_ratio", {})
    return {
        "ratio": data.get("q4_2025"),
        "trend": data.get("trend", "unknown"),
    }


def earnings_dashboard() -> list[dict]:
    """Consolidated per-ticker earnings dashboard.

    Merges forward claims, thesis signals, and SemiAnalysis signals
    into one row per deep-dive ticker.
    """
    thesis = load_thesis()
    ticker_map = thesis.get("ticker_map", {})
    _, _, semi = get_sources()

    companies = _load_company_yamls()

    # Build per-ticker rollup
    ticker_data = {}
    for company in companies:
        ticker = company.get("ticker", "?")
        quarter = company.get("quarter", "?")

        claims = company.get("forward_claims", [])
        pending = sum(1 for c in claims if c.get("status") == "pending")
        confirmed = sum(1 for c in claims if c.get("status") == "confirmed")
        missed = sum(1 for c in claims if c.get("status") == "missed")

        signals = company.get("thesis_signals", [])
        confirms = sum(1 for s in signals if s.get("direction") == "confirms")
        contradicts = sum(1 for s in signals if s.get("direction") == "contradicts")

        ticker_data[ticker] = {
            "ticker": ticker,
            "quarter": quarter,
            "next_earnings": ticker_map.get(ticker, {}).get("next_earnings"),
            "claims_pending": pending,
            "claims_confirmed": confirmed,
            "claims_missed": missed,
            "signals_confirms": confirms,
            "signals_contradicts": contradicts,
            "semi_signals": [],
        }

    # Add SemiAnalysis signals per ticker
    for ticker in ticker_data:
        s = semi.lookup(ticker)
        if s and "signals" in s:
            ticker_data[ticker]["semi_signals"] = s["signals"][:2]  # top 2

    return sorted(ticker_data.values(), key=lambda x: x.get("next_earnings") or "9999")


def _load_company_yamls() -> list[dict]:
    """Load all company quarter YAMLs from data/companies/."""
    results = []
    if not COMPANIES_DIR.exists():
        return results
    for ticker_dir in sorted(COMPANIES_DIR.iterdir()):
        if not ticker_dir.is_dir():
            continue
        for qfile in sorted(ticker_dir.glob("q*.yaml")):
            with open(qfile) as f:
                data = yaml.safe_load(f) or {}
            data["_file"] = str(qfile.relative_to(DATA_DIR.parent))
            results.append(data)
    return results


def forward_claims_due() -> list[dict]:
    """Collect all forward claims from company YAMLs, grouped by status."""
    companies = _load_company_yamls()
    claims = []
    for company in companies:
        ticker = company.get("ticker", "?")
        quarter = company.get("quarter", "?")
        for claim in company.get("forward_claims", []):
            claims.append({
                "ticker": ticker,
                "quarter": quarter,
                "claim": claim.get("claim", ""),
                "speaker": claim.get("speaker", ""),
                "verify_at": claim.get("verify_at", ""),
                "status": claim.get("status", "pending"),
                "notes": claim.get("notes", ""),
            })
    # Sort: pending first, then by verify_at
    claims.sort(key=lambda c: (
        0 if c["status"] == "pending" else 1,
        c["verify_at"],
    ))
    return claims


def earnings_signals() -> list[dict]:
    """Collect thesis_signals from all company YAMLs."""
    companies = _load_company_yamls()
    signals = []
    for company in companies:
        ticker = company.get("ticker", "?")
        quarter = company.get("quarter", "?")
        for sig in company.get("thesis_signals", []):
            signals.append({
                "ticker": ticker,
                "quarter": quarter,
                "bottleneck": sig.get("bottleneck", ""),
                "direction": sig.get("direction", ""),
                "evidence": sig.get("evidence", "").strip(),
            })
    return signals


def concept_drift() -> list[dict]:
    """Check for drift between wiki concept pages and thesis.yaml signals.

    Finds thesis.yaml signals that aren't reflected in the corresponding
    concept page, and company earnings signals not mentioned in concepts.
    """
    thesis = load_thesis()
    cascade = thesis.get("cascade", [])
    findings = []

    for stage in cascade:
        name = stage["name"]
        concept_file = STAGE_TO_CONCEPT.get(name)
        if not concept_file:
            continue

        concept_path = WIKI_DIR / "concepts" / f"{concept_file}.md"
        if not concept_path.exists():
            findings.append({
                "type": "missing_concept",
                "stage": name,
                "detail": f"No concept page for cascade stage '{name}'",
            })
            continue

        concept_text = concept_path.read_text().lower()

        # Check for thesis.yaml signals not mentioned in concept page
        for signal in stage.get("signals", []):
            # Extract key phrases from the signal (numbers, percentages, names)
            key_phrases = re.findall(r'\d+[%xBMGW]+|\$[\d.]+|\d+(?:\.\d+)?[x%]', signal)
            # Also check for distinctive words (3+ chars, not common)
            if not key_phrases:
                # Fall back to checking if a substantial substring appears
                words = [w for w in signal.lower().split() if len(w) > 5]
                key_phrases = words[:3]

            found = any(kp.lower() in concept_text for kp in key_phrases)
            if not found:
                findings.append({
                    "type": "thesis_signal_missing",
                    "stage": name,
                    "detail": signal.strip(),
                    "concept_page": f"concepts/{concept_file}.md",
                })

    # Check company earnings signals not reflected in any concept page
    all_concept_text = ""
    for cp in (WIKI_DIR / "concepts").glob("*.md"):
        all_concept_text += cp.read_text().lower() + "\n"

    companies = _load_company_yamls()
    for company in companies:
        ticker = company.get("ticker", "?")
        quarter = company.get("quarter", "?")
        for sig in company.get("thesis_signals", []):
            bottleneck = sig.get("bottleneck", "")
            evidence = sig.get("evidence", "").strip()
            # Check if any distinctive part of the evidence appears in concepts
            key_numbers = re.findall(r'\$[\d.]+[BMT]|\d+[%xBMGW]+', evidence)
            if key_numbers and not any(kn.lower() in all_concept_text for kn in key_numbers):
                findings.append({
                    "type": "earnings_signal_missing",
                    "stage": bottleneck,
                    "ticker": ticker,
                    "quarter": quarter,
                    "detail": evidence[:120],
                })

    return findings


def alignment_drift() -> list[dict]:
    """Check raw/source/data/thesis alignment across the canonical truth lane."""
    findings = []

    if not WIKI_RAW_DIR.exists():
        findings.append({
            "type": "missing_directory",
            "artifact": "wiki/raw/",
            "detail": "Schema and earnings source pages reference wiki/raw/, but the directory is absent.",
        })

    # Every cited upstream source must resolve from the wiki root.
    wiki_pages = sorted(WIKI_SOURCES_DIR.glob("*.md")) + sorted(WIKI_CONCEPTS_DIR.glob("*.md"))
    for page in wiki_pages:
        frontmatter = _load_frontmatter(page)
        source_refs = frontmatter.get("sources", [])
        if isinstance(source_refs, str):
            source_refs = [source_refs]

        for ref in source_refs:
            target = (WIKI_DIR / str(ref)).resolve()
            if not target.exists():
                findings.append({
                    "type": "missing_source_artifact",
                    "artifact": str(ref),
                    "path": str(page.relative_to(WIKI_DIR.parent)),
                    "detail": f"{page.relative_to(WIKI_DIR.parent)} cites a missing upstream source.",
                })

    companies = _load_company_yamls()
    company_by_slug = {
        _company_source_slug(company): company
        for company in companies
        if company.get("ticker") and company.get("quarter")
    }
    structured_tickers = {company.get("ticker") for company in companies if company.get("ticker")}

    earnings_source_pages = {}
    for page in sorted(WIKI_SOURCES_DIR.glob("*.md")):
        frontmatter = _load_frontmatter(page)
        tags = {str(tag).lower() for tag in frontmatter.get("tags", [])}
        if "earnings" in tags:
            earnings_source_pages[page.stem] = page

    # Every earnings source page should have a structured company twin.
    for slug, page in earnings_source_pages.items():
        if slug not in company_by_slug:
            findings.append({
                "type": "missing_company_yaml",
                "artifact": _expected_company_yaml_from_source_slug(slug),
                "path": str(page.relative_to(WIKI_DIR.parent)),
                "detail": "Earnings source page exists without a matching data/companies/ YAML.",
            })

    # Every structured company quarter should have a wiki source twin.
    for slug, company in company_by_slug.items():
        if slug not in earnings_source_pages:
            findings.append({
                "type": "missing_source_page",
                "ticker": company.get("ticker"),
                "artifact": _expected_source_page_from_company(company),
                "detail": "Structured company YAML exists without a matching wiki/sources/ earnings page.",
            })

    # Deep-dive tickers are expected to move through the full earnings funnel.
    thesis = load_thesis()
    ticker_map = thesis.get("ticker_map", {})
    for ticker in sorted(DEEP_DIVE_TICKERS):
        if ticker in structured_tickers:
            continue
        meta = ticker_map.get(ticker, {})
        findings.append({
            "type": "deep_dive_missing_company_data",
            "ticker": ticker,
            "stage": meta.get("bottleneck", ""),
            "artifact": f"data/companies/{ticker}/",
            "detail": "Deep-dive ticker is missing structured company coverage.",
        })

    # Ticker-level bottlenecks should have an explainer page somewhere in concepts/.
    for bottleneck, concept_slug in sorted(BOTTLENECK_TO_CONCEPT.items()):
        related_tickers = sorted(
            ticker
            for ticker, meta in ticker_map.items()
            if meta.get("bottleneck") == bottleneck or meta.get("also") == bottleneck
        )
        if not related_tickers:
            continue

        concept_path = WIKI_CONCEPTS_DIR / f"{concept_slug}.md"
        if not concept_path.exists():
            findings.append({
                "type": "missing_bottleneck_concept",
                "stage": bottleneck,
                "artifact": f"wiki/concepts/{concept_slug}.md",
                "detail": f"No concept page covers bottleneck '{bottleneck}' for {', '.join(related_tickers)}.",
            })

    findings.extend(concept_drift())
    findings.sort(
        key=lambda finding: (
            finding.get("type", ""),
            finding.get("stage", ""),
            finding.get("ticker", ""),
            finding.get("artifact", ""),
            finding.get("detail", ""),
        )
    )
    return findings


BOTTLENECK_ONE_LINERS = {
    "CoWoS packaging": "Chip-on-wafer stacking for GPU+HBM. TSMC monopoly. Resolved.",
    "Power / DC buildout": "Data centers need power + cooling. 2-3yr build. Miners converting.",
    "Memory supercycle": "AI consumes all HBM/DRAM. Prices +90% QoQ. All vendors sold out.",
    "N3 logic wafers": "TSMC 3nm at 100%+ util. Every AI chip competes for same lines.",
    "Pluggable optics (scale-out)": "800G/1.6T transceivers in every GPU rack. Revenue flowing now.",
    "Co-packaged optics / CPO (scale-up)": "Laser-on-chip for next-gen racks. Volume 2028+.",
    "EUV tools": "ASML monopoly. ~100 tools/yr ceiling. Final cascade bottleneck.",
}

BOTTLENECK_EXPLAINERS = {
    "CoWoS packaging": (
        "CoWoS (Chip-on-Wafer-on-Substrate) is how you physically stack an AI chip "
        "on top of the high-bandwidth memory (HBM) it needs. Think of it like building "
        "a tiny skyscraper on a silicon wafer — the chip sits on one floor, memory on "
        "another, all connected by thousands of microscopic wires. Only TSMC can do this "
        "at scale. When AI chip demand exploded in 2023, TSMC didn't have enough CoWoS "
        "capacity to package all the chips Nvidia wanted — you could make the chips but "
        "couldn't assemble them. This bottleneck has since been resolved."
    ),
    "Power / DC buildout": (
        "AI data centers consume enormous amounts of electricity — a single Nvidia GPU "
        "rack draws as much power as ~30 homes. Training a frontier AI model can require "
        "a dedicated power plant. The bottleneck: you can buy GPUs, but if there's no "
        "power grid connection, no cooling infrastructure, and no physical building to "
        "put them in, they sit in a warehouse. Data centers take 2-3 years to build. "
        "Power interconnects can take 5+ years. This is why Leopold is betting on bitcoin "
        "miners — they already have land, grid connections, and cooling, and can convert "
        "to AI data centers much faster than building from scratch."
    ),
    "Memory supercycle": (
        "Every AI chip needs memory (DRAM/HBM) to hold the data it's processing. HBM "
        "(High Bandwidth Memory) is special memory stacked in layers and bonded directly "
        "to the GPU — it's 85% less dense than regular DRAM and much harder to make. "
        "The problem: AI is consuming so much memory that there isn't enough left for "
        "phones, PCs, and other devices. DRAM prices have surged 90-95% in a single "
        "quarter. In an unprecedented twist, regular DDR4 memory now costs MORE per bit "
        "than the exotic HBM3e used in AI chips. Every major memory maker (SK Hynix, "
        "Samsung, Micron) is sold out through 2026."
    ),
    "N3 logic wafers": (
        "N3 refers to TSMC's 3-nanometer manufacturing process — the most advanced way "
        "to make chips. Every major AI accelerator (Nvidia Rubin, Google TPU v7, Amazon "
        "Trainium3, AMD MI350X) is moving to N3 simultaneously in 2026. But TSMC only "
        "has so many N3 production lines, and they're running at 100%+ utilization. "
        "AI already consumes 60% of N3 output and is projected to take 86% by 2027. "
        "This means AI chips are literally crowding out smartphone chips — Apple, "
        "Qualcomm, and MediaTek all compete for the same production lines. This is why "
        "Baker is massively long NVIDIA ($1B+) — if supply is constrained, the company "
        "with the strongest demand (Nvidia) has pricing power."
    ),
    "Optical interconnect / CPO": (
        "As AI clusters grow from hundreds to thousands to tens of thousands of GPUs, "
        "the copper cables connecting them can't keep up — they're too slow and generate "
        "too much heat. Co-Packaged Optics (CPO) replaces copper with laser light, "
        "transmitting data between racks at the speed of light. Nvidia's next-gen Rubin "
        "Ultra architecture (NVL576+) literally requires CPO to function — copper can't "
        "handle the bandwidth between racks. This is projected to become a $20B market "
        "by 2036. It's the ONLY bottleneck where all three sources agree: Leopold holds "
        "LITE and COHR, Baker holds COHR, CIEN, and ALAB, and SemiAnalysis has flagged "
        "2026 as the inflection year."
    ),
    "EUV tools": (
        "EUV (Extreme Ultraviolet Lithography) machines are made by exactly one company "
        "in the world: ASML, using optics from exactly one supplier: Zeiss. These $350M+ "
        "machines use ultraviolet light to etch circuit patterns onto silicon wafers. "
        "Every advanced chip (N3, N2) requires EUV. ASML can only produce about 100 of "
        "these machines per year by 2030 — that's a hard physical ceiling set by Zeiss's "
        "ability to make the optics. If AI demand keeps growing, there won't be enough "
        "EUV tools to build enough fabs to make enough chips. This is the final "
        "bottleneck in the cascade — the one nobody can solve with money alone."
    ),
}


def generate_summary(cascade: list[dict], agreements: list[dict], divs: list[dict]) -> str:
    """Generate a plain-language summary of the current thesis state."""
    # Find active bottlenecks
    active = [s for s in cascade if s["status"] in ("active", "active_emerging")]
    full_agree = [a for a in agreements if a["agreement"] == "full"]
    full_agree_tickers = ", ".join(a["ticker"] for a in full_agree)

    # Total exposure
    l_total = sum(s.get("leopold_exposure", 0) for s in cascade)
    b_total = sum(s.get("baker_exposure", 0) for s in cascade)

    active_names = " and ".join(s["name"] for s in active)

    summary = (
        f"<strong>Where we are:</strong> The semiconductor supply chain has a sequence of physical "
        f"constraints that limit how fast AI can scale. Each one gets solved eventually, but the next "
        f"one becomes the new ceiling. Right now, <strong>{active_names}</strong> are the active "
        f"constraints — they're happening simultaneously, not sequentially as originally expected."
    )

    summary += (
        f"<br><br><strong>What the money says:</strong> Leopold Aschenbrenner's fund ($5.5B) and "
        f"Gavin Baker's fund ($8.2B) are both betting heavily on AI infrastructure but disagree on "
        f"<em>where</em> the constraint is tightest. Leopold has exited chip companies entirely and "
        f"loaded up on power infrastructure and GPU cloud operators. Baker has done the opposite — "
        f"$1B+ in Nvidia alone — betting that chips themselves remain scarce. The only place they "
        f"fully agree is <strong>optical interconnect ({full_agree_tickers})</strong>, which makes "
        f"it the highest-conviction, lowest-divergence-risk zone in the entire thesis."
    )

    return summary


def generate_explainers(cascade: list[dict]) -> str:
    """Generate plain-language explainers for each cascade stage."""
    html = ""
    for stage in cascade:
        name = stage["name"]
        explainer = BOTTLENECK_EXPLAINERS.get(name, "")
        if not explainer:
            continue

        icon = {
            "played_out": "&#9989;",
            "active": "&#128308;",
            "active_emerging": "&#128992;",
            "emerging": "&#128993;",
            "next": "&#11093;",
        }.get(stage["status"], "&#9675;")

        status_label = stage["status"].replace("_", " ").title()

        html += f"""
        <div class="explainer">
            <div class="explainer-header">{icon} {name} <span class="explainer-status">({status_label})</span></div>
            <p>{explainer}</p>
        </div>"""

    return html


def cascade_status() -> list[dict]:
    """Return the current bottleneck cascade with source positioning overlaid."""
    thesis = load_thesis()
    leopold, baker, semi = get_sources()

    results = []
    for stage in thesis.get("cascade", []):
        stage_tickers = stage.get("tickers", [])

        leopold_exposure = sum(
            (leopold.lookup(t) or {}).get("value", 0) for t in stage_tickers
        )
        baker_exposure = sum(
            (baker.lookup(t) or {}).get("value", 0) for t in stage_tickers
        )
        semi_signal_count = sum(
            len((semi.lookup(t) or {}).get("signals", [])) for t in stage_tickers
        )

        results.append({
            "name": stage["name"],
            "status": stage["status"],
            "period": stage.get("period"),
            "tickers": stage_tickers,
            "signals": stage.get("signals", []),
            "leopold_exposure": leopold_exposure,
            "baker_exposure": baker_exposure,
            "semi_signals": semi_signal_count,
        })

    return results
