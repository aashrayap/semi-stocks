"""Report generator — builds an HTML report from synthesis data.

Restructured: 5 sections (from original 9).
1. Summary
2. Cascade + Cycle Risk (merged cascade, explainers, cycle assessment)
3. Positions + Signals (merged agreement map, divergences inline)
4. Earnings Dashboard (merged forward claims, earnings signals, SemiAnalysis)
5. Drift (collapsed footer)
"""

import json
from datetime import date, datetime
from pathlib import Path

from src.synthesis import (
    BOTTLENECK_ONE_LINERS,
    agreement_map,
    baker_hedge_ratio,
    cascade_status,
    concept_drift,
    cycle_assessment,
    divergences,
    earnings_dashboard,
    earnings_signals,
    forward_claims_due,
    generate_summary,
    get_sources,
    load_thesis,
)

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def _fmt_value(val: int | None) -> str:
    """Format a dollar value for display."""
    if val is None or val == 0:
        return "—"
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:.1f}B"
    if val >= 1_000_000:
        return f"${val / 1_000_000:.0f}M"
    return f"${val:,.0f}"


def _fmt_pct(val: float | None) -> str:
    if val is None:
        return "—"
    return f"{val * 100:.1f}%"


def _status_icon(status: str) -> str:
    icons = {
        "played_out": "&#9989;",       # checkmark
        "active": "&#128308;",          # red circle
        "active_emerging": "&#128992;", # orange circle
        "emerging": "&#128993;",        # yellow circle
        "next": "&#11093;",             # white circle
    }
    return icons.get(status, "&#9675;")


def _cycle_badge(phase: str, action: str) -> str:
    """Return a color-coded cycle phase badge."""
    colors = {
        "peak_shortage":  ("#da3633", "#fff"),   # red
        "mid_shortage":   ("#f0883e", "#fff"),   # orange
        "early_cycle":    ("#238636", "#fff"),   # green
        "post_peak":      ("#9e6a03", "#fff"),   # amber
        "pre_cycle":      ("#21262d", "#8b949e"),# gray
        "resolved":       ("#21262d", "#8b949e"),# gray
    }
    bg, fg = colors.get(phase, ("#21262d", "#8b949e"))
    return f'<span class="badge" style="background:{bg};color:{fg}">{action}</span>'


def _agreement_dots(held_by: list[str]) -> str:
    l = "&#9679;" if "leopold" in held_by else "&#9675;"
    b = "&#9679;" if "baker" in held_by else "&#9675;"
    s = "&#9679;" if "semianalysis" in held_by else "&#9675;"
    return f"L{l} B{b} S{s}"


def generate_html() -> str:
    """Generate the full HTML report."""
    leopold, baker, semi = get_sources()
    cascade = cascade_status()
    agreements = agreement_map()
    divs = divergences()
    cycle = cycle_assessment()
    hedge = baker_hedge_ratio()
    dashboard = earnings_dashboard()
    thesis = load_thesis()

    leopold_summary = leopold.summary()
    baker_summary = baker.summary()

    today = date.today().strftime("%B %d, %Y")

    # Build summary
    summary_html = generate_summary(cascade, agreements, divs)

    # Add cycle risk sentence to summary
    peak_stages = [c for c in cycle if c["cycle_phase"] == "peak_shortage"]
    if peak_stages:
        peak_names = ", ".join(s["name"] for s in peak_stages)
        hedge_pct = int((hedge.get("ratio") or 0) * 100)
        summary_html += (
            f"<br><br><strong>Cycle risk:</strong> <span style='color:#da3633'>{peak_names}</span> "
            f"{'is' if len(peak_stages) == 1 else 'are'} at peak shortage — Baker's framework says "
            f"hedge, don't exit. His QQQ put hedge ratio: <strong>{hedge_pct}%</strong> "
            f"(trend: {hedge.get('trend', '?')})."
        )

    # ── SECTION 2: CASCADE + CYCLE RISK ──
    cascade_rows = ""
    for i, stage in enumerate(cascade):
        icon = _status_icon(stage["status"])
        l_exp = _fmt_value(stage["leopold_exposure"])
        b_exp = _fmt_value(stage["baker_exposure"])
        tickers_str = ", ".join(stage["tickers"])
        one_liner = BOTTLENECK_ONE_LINERS.get(stage["name"], "")

        # Get cycle data
        c = cycle[i] if i < len(cycle) else {}
        phase = c.get("cycle_phase", "")
        action = c.get("cycle_action", "")
        cycle_cell = _cycle_badge(phase, action) if phase else "—"
        cycle_sig = c.get("cycle_signal", "")

        # Cycle risk flags as expandable list
        flags = c.get("cycle_risk_flags", [])
        flag_count = len(flags)
        flag_cell = ""
        if flag_count > 0:
            flag_items = "".join(f"<li>{f}</li>" for f in flags)
            flag_cell = (
                f'<details class="flag-details">'
                f'<summary style="color:#da3633;cursor:pointer;font-size:12px">&#9888; {flag_count}</summary>'
                f'<ul class="flag-list">{flag_items}</ul>'
                f'</details>'
            )

        cascade_rows += f"""
        <tr>
            <td>{icon} {stage['name']}<br><span class="small">{one_liner}</span></td>
            <td>{cycle_cell}</td>
            <td class="small">{cycle_sig}</td>
            <td>{tickers_str}</td>
            <td>{l_exp}</td>
            <td>{b_exp}</td>
            <td>{flag_cell}</td>
        </tr>"""

    # ── SECTION 3: POSITIONS + SIGNALS (merged agreement + divergences) ──
    # Build a divergence lookup for inline badges
    div_lookup = {}
    for d in divs:
        if d["type"] == "directional":
            div_lookup[d["ticker"]] = "directional"

    # Check for trim/add divergences (Baker trimming while Leopold adding)
    baker_positions = {}
    for ticker_key in thesis.get("ticker_map", {}):
        b = baker.lookup(ticker_key)
        if b and b.get("change_vs_prior"):
            baker_positions[ticker_key] = b["change_vs_prior"]

    agreement_rows = ""
    today_dt = date.today()
    for a in agreements:
        dots = _agreement_dots(a["held_by"])
        l_val = _fmt_value(a["leopold_value"])
        b_val = _fmt_value(a["baker_value"])

        # Agreement badge with divergence override
        if a["ticker"] in div_lookup:
            badge = '<span class="badge" style="background:#da3633;color:#fff">DIVERGE</span>'
        else:
            badge = {
                "full": '<span class="badge full">AGREE</span>',
                "partial": '<span class="badge partial">PARTIAL</span>',
                "single": '<span class="badge single">SINGLE</span>',
            }[a["agreement"]]

        # Format earnings date with urgency coloring
        ne = a.get("next_earnings")
        if ne:
            try:
                ne_dt = datetime.strptime(ne, "%Y-%m-%d").date()
                days_out = (ne_dt - today_dt).days
                ne_display = ne_dt.strftime("%b %d")
                if days_out <= 7:
                    ne_cell = f'<span style="color:#da3633;font-weight:600">{ne_display}</span>'
                elif days_out <= 21:
                    ne_cell = f'<span style="color:#f0883e">{ne_display}</span>'
                else:
                    ne_cell = ne_display
            except ValueError:
                ne_cell = ne
        else:
            ne_cell = "—"

        agreement_rows += f"""
        <tr>
            <td><strong>{a['ticker']}</strong></td>
            <td>{a['bottleneck']}</td>
            <td>{dots}</td>
            <td>{badge}</td>
            <td>{l_val}</td>
            <td>{b_val}</td>
            <td>{ne_cell}</td>
            <td>{a['semi_signals']}</td>
        </tr>"""

    # ── SECTION 4: EARNINGS DASHBOARD ──
    dash_rows = ""
    for d in dashboard:
        ne = d.get("next_earnings")
        if ne:
            try:
                ne_dt = datetime.strptime(ne, "%Y-%m-%d").date()
                days_out = (ne_dt - today_dt).days
                ne_display = ne_dt.strftime("%b %d")
                if days_out <= 7:
                    ne_cell = f'<span style="color:#da3633;font-weight:600">{ne_display} ({days_out}d)</span>'
                elif days_out <= 21:
                    ne_cell = f'<span style="color:#f0883e">{ne_display} ({days_out}d)</span>'
                else:
                    ne_cell = f'{ne_display} ({days_out}d)'
            except ValueError:
                ne_cell = ne
        else:
            ne_cell = "—"

        claims_summary = ""
        if d["claims_pending"]:
            claims_summary += f'{d["claims_pending"]} pending'
        if d["claims_confirmed"]:
            claims_summary += f', {d["claims_confirmed"]} confirmed'
        if d["claims_missed"]:
            claims_summary += f', <span style="color:#da3633">{d["claims_missed"]} missed</span>'
        if not claims_summary:
            claims_summary = "—"

        signals_summary = ""
        if d["signals_confirms"]:
            signals_summary += f'&#9989; {d["signals_confirms"]}'
        if d["signals_contradicts"]:
            signals_summary += f' &#10060; {d["signals_contradicts"]}'
        if not signals_summary:
            signals_summary = "—"

        semi_summary = ""
        for sig in d.get("semi_signals", []):
            semi_summary += f"&bull; {sig[:60]}...<br>" if len(sig) > 60 else f"&bull; {sig}<br>"
        if not semi_summary:
            semi_summary = "—"

        dash_rows += f"""
        <tr>
            <td><strong>{d['ticker']}</strong></td>
            <td>{d.get('quarter', '—')}</td>
            <td>{ne_cell}</td>
            <td>{claims_summary}</td>
            <td>{signals_summary}</td>
            <td class="small">{semi_summary}</td>
        </tr>"""

    # ── SECTION 5: DRIFT (collapsed) ──
    drift = concept_drift()
    drift_count = len(drift)
    drift_rows = ""
    for d in drift:
        dtype = d["type"].replace("_", " ").title()
        ticker = d.get("ticker", "")
        stage = d.get("stage", "")
        concept = d.get("concept_page", "")
        detail = d.get("detail", "")
        drift_rows += f"""
        <tr>
            <td>{dtype}</td>
            <td>{stage}</td>
            <td>{ticker}</td>
            <td>{concept}</td>
            <td class="small">{detail[:120]}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>semi-stocks | {today}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, 'SF Mono', monospace; background: #0d1117; color: #c9d1d9; padding: 24px; }}
    h1 {{ color: #58a6ff; font-size: 20px; margin-bottom: 4px; }}
    h2 {{ color: #8b949e; font-size: 14px; margin-bottom: 20px; font-weight: normal; }}
    h3 {{ color: #f0f6fc; font-size: 15px; margin: 28px 0 12px 0; padding-bottom: 6px; border-bottom: 1px solid #21262d; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; }}
    th {{ text-align: left; padding: 8px 10px; background: #161b22; color: #8b949e; font-weight: 600; border-bottom: 1px solid #21262d; }}
    td {{ padding: 6px 10px; border-bottom: 1px solid #21262d; vertical-align: top; }}
    tr:hover {{ background: #161b22; }}
    .badge {{ padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }}
    .badge.full {{ background: #238636; color: #fff; }}
    .badge.partial {{ background: #9e6a03; color: #fff; }}
    .badge.single {{ background: #21262d; color: #8b949e; }}
    .badge.missed {{ background: #da3633; color: #fff; }}
    .meta {{ display: flex; gap: 32px; margin-bottom: 20px; font-size: 13px; color: #8b949e; }}
    .meta strong {{ color: #c9d1d9; }}
    .small {{ font-size: 11px; color: #8b949e; line-height: 1.5; }}
    .section {{ margin-bottom: 32px; }}
    .summary {{ background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 16px 20px; margin-bottom: 28px; font-size: 13px; line-height: 1.7; }}
    .summary strong {{ color: #58a6ff; }}
    .summary em {{ color: #f0883e; font-style: normal; }}
    details {{ margin-bottom: 20px; }}
    details summary {{ cursor: pointer; color: #8b949e; font-size: 13px; padding: 8px 0; }}
    details summary:hover {{ color: #c9d1d9; }}
    .flag-details summary {{ padding: 0; font-size: 12px; }}
    .flag-list {{ margin: 6px 0 0 16px; padding: 0; font-size: 11px; color: #f0883e; line-height: 1.6; }}
    .flag-list li {{ margin-bottom: 2px; }}
</style>
</head>
<body>

<h1>semi-stocks</h1>
<h2>Semiconductor bottleneck research | {today}</h2>

<div class="meta">
    <div><strong>Leopold</strong> {leopold_summary.get('quarter', '')} | AUM {_fmt_value(leopold_summary.get('aum'))} | Filed {leopold_summary.get('filed', '')} | {leopold_summary.get('positions_count', '')} positions</div>
    <div><strong>Baker</strong> {baker_summary.get('quarter', '')} | AUM {_fmt_value(baker_summary.get('aum'))} | Filed {baker_summary.get('filed', '')} | {baker_summary.get('positions_count', '')} positions</div>
</div>

<div class="summary">
{summary_html}
</div>

<div class="section">
<h3>CASCADE + CYCLE RISK</h3>
<table>
    <tr><th>Stage</th><th>Cycle</th><th>Signal</th><th>Tickers</th><th>Leopold $</th><th>Baker $</th><th>Flags</th></tr>
    {cascade_rows}
</table>
</div>

<div class="section">
<h3>POSITIONS + SIGNALS</h3>
<table>
    <tr><th>Ticker</th><th>Bottleneck</th><th>Sources</th><th>Agreement</th><th>Leopold</th><th>Baker</th><th>Earnings</th><th>Semi#</th></tr>
    {agreement_rows}
</table>
</div>

{"" if not dash_rows else f'''<div class="section">
<h3>EARNINGS DASHBOARD</h3>
<table>
    <tr><th>Ticker</th><th>Quarter</th><th>Next Earnings</th><th>Forward Claims</th><th>Thesis Signals</th><th>SemiAnalysis</th></tr>
    {dash_rows}
</table>
</div>'''}

{"" if drift_count == 0 else f'''<details class="section">
<summary>DRIFT WARNINGS ({drift_count} findings)</summary>
<table>
    <tr><th>Type</th><th>Stage</th><th>Ticker</th><th>Concept Page</th><th>Detail</th></tr>
    {drift_rows}
</table>
</details>'''}

</body>
</html>"""

    return html


def build_report() -> Path:
    """Generate and save the HTML report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    html = generate_html()
    out = REPORTS_DIR / "latest.html"
    out.write_text(html)
    return out


if __name__ == "__main__":
    path = build_report()
    print(f"Report written to {path}")
