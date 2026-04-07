"""Synthesis engine — cross-source agreement, divergence, and thesis mapping."""

import re
import yaml
from pathlib import Path

from src.sources.base import DATA_DIR
from src.sources.fund_13f import Fund13FSource
from src.sources.semianalysis import SemiAnalysisSource

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
COMPANIES_DIR = DATA_DIR / "companies"

# Map cascade stage names to concept page filenames
STAGE_TO_CONCEPT = {
    "Memory supercycle": "memory-supercycle",
    "N3 logic wafers": "n3-wafer-crunch",
    "Pluggable optics (scale-out)": "pluggable-optics",
    "Co-packaged optics / CPO (scale-up)": "co-packaged-optics",
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
