"""Report generator — builds an HTML report from synthesis data."""

import json
from datetime import date, datetime
from pathlib import Path

from src.synthesis import (
    agreement_map,
    cascade_status,
    concept_drift,
    divergences,
    earnings_signals,
    forward_claims_due,
    generate_explainers,
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
    thesis = load_thesis()

    leopold_summary = leopold.summary()
    baker_summary = baker.summary()

    today = date.today().strftime("%B %d, %Y")

    # Build summary and explainers
    summary_html = generate_summary(cascade, agreements, divs)
    explainers_html = generate_explainers(cascade)

    # Build cascade rows
    cascade_rows = ""
    for stage in cascade:
        icon = _status_icon(stage["status"])
        l_exp = _fmt_value(stage["leopold_exposure"])
        b_exp = _fmt_value(stage["baker_exposure"])
        tickers_str = ", ".join(stage["tickers"])
        cascade_rows += f"""
        <tr>
            <td>{icon} {stage['name']}</td>
            <td>{stage['status'].replace('_', ' ')}</td>
            <td>{stage.get('period', '')}</td>
            <td>{tickers_str}</td>
            <td>{l_exp}</td>
            <td>{b_exp}</td>
            <td>{stage['semi_signals']}</td>
        </tr>"""

    # Build agreement rows
    agreement_rows = ""
    today_dt = date.today()
    for a in agreements:
        dots = _agreement_dots(a["held_by"])
        l_val = _fmt_value(a["leopold_value"])
        b_val = _fmt_value(a["baker_value"])
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

    # Build divergence rows
    divergence_rows = ""
    for d in divs:
        if d["type"] == "leopold_only":
            divergence_rows += f"""
            <tr>
                <td><strong>{d['ticker']}</strong></td>
                <td>Leopold only</td>
                <td>{_fmt_value(d.get('leopold_value'))} ({_fmt_pct(d.get('leopold_pct'))})</td>
                <td>—</td>
                <td>{d.get('notes', '')}</td>
            </tr>"""
        elif d["type"] == "baker_only":
            divergence_rows += f"""
            <tr>
                <td><strong>{d['ticker']}</strong></td>
                <td>Baker only</td>
                <td>—</td>
                <td>{_fmt_value(d.get('baker_value'))} ({_fmt_pct(d.get('baker_pct'))})</td>
                <td>{d.get('notes', '')}</td>
            </tr>"""
        elif d["type"] == "directional":
            divergence_rows += f"""
            <tr>
                <td><strong>{d['ticker']}</strong></td>
                <td>Directional</td>
                <td>{d.get('leopold', '')}</td>
                <td>{d.get('baker', '')}</td>
                <td></td>
            </tr>"""

    # Forward claims dashboard
    claims = forward_claims_due()
    pending_claims = [c for c in claims if c["status"] == "pending"]
    resolved_claims = [c for c in claims if c["status"] != "pending"]

    claims_rows = ""
    for c in pending_claims:
        claims_rows += f"""
        <tr>
            <td><strong>{c['ticker']}</strong></td>
            <td>{c['quarter']}</td>
            <td class="small">{c['claim']}</td>
            <td>{c['verify_at']}</td>
            <td><span class="badge partial">PENDING</span></td>
        </tr>"""
    for c in resolved_claims:
        status_class = {"confirmed": "full", "missed": "missed", "revised": "partial"}.get(c["status"], "single")
        status_label = c["status"].upper()
        claims_rows += f"""
        <tr>
            <td><strong>{c['ticker']}</strong></td>
            <td>{c['quarter']}</td>
            <td class="small">{c['claim']}</td>
            <td>{c['verify_at']}</td>
            <td><span class="badge {status_class}">{status_label}</span></td>
        </tr>"""

    # Earnings intelligence
    esignals = earnings_signals()
    esignal_rows = ""
    for s in esignals:
        direction_icon = "&#9989;" if s["direction"] == "confirms" else "&#10060;"
        esignal_rows += f"""
        <tr>
            <td><strong>{s['ticker']}</strong></td>
            <td>{s['quarter']}</td>
            <td>{s['bottleneck']}</td>
            <td>{direction_icon} {s['direction']}</td>
            <td class="small">{s['evidence'][:150]}</td>
        </tr>"""

    # Concept drift warnings
    drift = concept_drift()
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

    # Recent SemiAnalysis signals
    recent_signals = semi.recent(5)
    signal_rows = ""
    for s in recent_signals:
        pts = "<br>".join(f"&bull; {dp}" for dp in s.get("data_points", [])[:3])
        tickers_str = ", ".join(s.get("tickers", []))
        signal_rows += f"""
        <tr>
            <td>{s.get('date', '')}</td>
            <td>{s.get('title', '')}</td>
            <td>{s.get('bottleneck', '')}</td>
            <td>{tickers_str}</td>
            <td class="small">{pts}</td>
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
    .explainer {{ background: #0d1117; border-left: 3px solid #21262d; padding: 10px 16px; margin-bottom: 12px; font-size: 12px; line-height: 1.6; }}
    .explainer-header {{ font-size: 13px; font-weight: 600; color: #f0f6fc; margin-bottom: 4px; }}
    .explainer-status {{ font-weight: 400; color: #8b949e; font-size: 12px; }}
    .explainer p {{ color: #8b949e; margin: 0; }}
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
<h3>BOTTLENECK CASCADE</h3>
<table>
    <tr><th>Stage</th><th>Status</th><th>Period</th><th>Tickers</th><th>Leopold $</th><th>Baker $</th><th>Semi Signals</th></tr>
    {cascade_rows}
</table>
</div>

<div class="section">
<h3>WHAT EACH BOTTLENECK MEANS</h3>
{explainers_html}
</div>

<div class="section">
<h3>SOURCE AGREEMENT MAP</h3>
<table>
    <tr><th>Ticker</th><th>Bottleneck</th><th>Sources</th><th>Agreement</th><th>Leopold</th><th>Baker</th><th>Earnings</th><th>Semi Signals</th></tr>
    {agreement_rows}
</table>
</div>

<div class="section">
<h3>DIVERGENCES</h3>
<table>
    <tr><th>Ticker</th><th>Type</th><th>Leopold</th><th>Baker</th><th>Notes</th></tr>
    {divergence_rows}
</table>
</div>

<div class="section">
<h3>FORWARD CLAIMS SCORECARD</h3>
<table>
    <tr><th>Ticker</th><th>Quarter</th><th>Claim</th><th>Verify At</th><th>Status</th></tr>
    {claims_rows}
</table>
</div>

<div class="section">
<h3>EARNINGS INTELLIGENCE</h3>
<table>
    <tr><th>Ticker</th><th>Quarter</th><th>Bottleneck</th><th>Direction</th><th>Evidence</th></tr>
    {esignal_rows}
</table>
</div>

{"" if not drift_rows else f'''<div class="section">
<h3>DRIFT WARNINGS</h3>
<p class="small" style="margin-bottom: 10px; color: #f0883e;">Signals in thesis.yaml or earnings data not reflected in wiki concept pages.</p>
<table>
    <tr><th>Type</th><th>Stage</th><th>Ticker</th><th>Concept Page</th><th>Detail</th></tr>
    {drift_rows}
</table>
</div>'''}

<div class="section">
<h3>RECENT SEMIANALYSIS SIGNALS</h3>
<table>
    <tr><th>Date</th><th>Title</th><th>Bottleneck</th><th>Tickers</th><th>Key Points</th></tr>
    {signal_rows}
</table>
</div>

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
