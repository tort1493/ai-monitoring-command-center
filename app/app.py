from __future__ import annotations

import html
import math
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from project.monitoring.service import build_demo_snapshot


SEVERITY_STYLES = {
    "critical": "#ff5d73",
    "high": "#ff9a3c",
    "medium": "#ffd166",
    "low": "#57c7ff",
}

STATUS_STYLES = {
    "healthy": "#73f0a8",
    "degraded": "#ffd166",
    "incident": "#ff5d73",
}

METRIC_OPTIONS = {
    "Latency p95": ("latency_p95_ms", "ms"),
    "Error Rate": ("error_rate", "%"),
    "Hallucination Risk": ("hallucination_risk", "%"),
    "Hourly Spend": ("spend_hourly_usd", "$"),
}


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #07111f;
            --panel: rgba(8, 20, 38, 0.86);
            --panel-strong: rgba(10, 24, 44, 0.97);
            --border: rgba(127, 168, 201, 0.18);
            --text: #eff6ff;
            --muted: #9fb4ca;
            --cyan: #57c7ff;
            --lime: #73f0a8;
            --amber: #ffd166;
            --danger: #ff5d73;
        }
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(87, 199, 255, 0.14), transparent 28%),
                radial-gradient(circle at top right, rgba(255, 209, 102, 0.12), transparent 24%),
                linear-gradient(180deg, #08101c 0%, #07111f 45%, #050c15 100%);
            color: var(--text);
        }
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2rem;
            max-width: 1320px;
        }
        h1, h2, h3 {
            color: var(--text);
            font-family: "Space Grotesk", "Segoe UI", sans-serif;
            letter-spacing: -0.02em;
        }
        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(9, 22, 40, 0.95), rgba(7, 17, 31, 0.92));
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
            color: var(--muted);
        }
        [data-testid="stMetricValue"] {
            color: var(--text);
            font-family: "Space Grotesk", "Segoe UI", sans-serif;
        }
        div[data-testid="stVerticalBlock"] div:has(> .command-panel) {
            width: 100%;
        }
        .command-hero {
            position: relative;
            overflow: hidden;
            padding: 1.5rem;
            border-radius: 26px;
            border: 1px solid var(--border);
            background:
                linear-gradient(135deg, rgba(6, 17, 31, 0.98), rgba(10, 25, 46, 0.9)),
                linear-gradient(90deg, rgba(87, 199, 255, 0.08), transparent);
            box-shadow: 0 22px 50px rgba(0, 0, 0, 0.24);
        }
        .command-hero::after {
            content: "";
            position: absolute;
            inset: auto -120px -120px auto;
            width: 280px;
            height: 280px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(87, 199, 255, 0.18), transparent 68%);
        }
        .eyebrow {
            display: inline-flex;
            gap: 0.5rem;
            align-items: center;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(87, 199, 255, 0.08);
            color: var(--cyan);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border: 1px solid rgba(87, 199, 255, 0.18);
        }
        .hero-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }
        .hero-title {
            margin: 0.65rem 0 0.3rem;
            font-size: 2.6rem;
            line-height: 1;
        }
        .hero-copy {
            color: var(--muted);
            max-width: 52rem;
            font-size: 1rem;
        }
        .hero-band {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin-top: 1rem;
        }
        .hero-pill {
            padding: 0.5rem 0.85rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.04);
            color: var(--text);
            border: 1px solid var(--border);
            font-size: 0.82rem;
        }
        .hero-stat {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.03);
        }
        .hero-stat-label {
            color: var(--muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .hero-stat-value {
            font-size: 2rem;
            font-weight: 700;
            margin-top: 0.35rem;
        }
        .panel {
            border: 1px solid var(--border);
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(8, 20, 38, 0.88), rgba(7, 17, 31, 0.92));
            padding: 1.1rem;
            box-shadow: 0 18px 36px rgba(0, 0, 0, 0.16);
        }
        .panel-title {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 1rem;
            margin-bottom: 0.8rem;
        }
        .panel-kicker {
            color: var(--muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .summary-line {
            color: var(--text);
            font-size: 1rem;
            margin: 0.3rem 0 0.9rem;
        }
        .recommendation {
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            padding: 0.75rem 0;
            border-top: 1px solid rgba(127, 168, 201, 0.12);
        }
        .recommendation:first-of-type {
            border-top: 0;
            padding-top: 0;
        }
        .recommendation-index {
            width: 1.6rem;
            height: 1.6rem;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(87, 199, 255, 0.12);
            color: var(--cyan);
            font-size: 0.8rem;
            font-weight: 700;
            flex: 0 0 auto;
        }
        .chart-shell {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.6rem 0.8rem 0.9rem;
            background: rgba(255, 255, 255, 0.02);
        }
        .chart-caption {
            display: flex;
            justify-content: space-between;
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 0.4rem;
        }
        .chart-meta {
            display: flex;
            gap: 0.7rem;
            margin-top: 0.55rem;
            color: var(--muted);
            font-size: 0.82rem;
        }
        .service-card {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.03);
            min-height: 220px;
        }
        .service-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 0.8rem;
        }
        .service-name {
            font-size: 1.1rem;
            font-weight: 700;
        }
        .service-owner {
            color: var(--muted);
            font-size: 0.88rem;
        }
        .status-chip {
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .service-metric {
            margin-top: 0.7rem;
        }
        .service-metric-head {
            display: flex;
            justify-content: space-between;
            color: var(--muted);
            font-size: 0.8rem;
            margin-bottom: 0.25rem;
        }
        .metric-bar {
            height: 9px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.06);
            overflow: hidden;
        }
        .metric-fill {
            height: 100%;
            border-radius: 999px;
        }
        .service-note {
            margin-top: 0.85rem;
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.5;
        }
        .alert-card, .timeline-card {
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            margin-bottom: 0.75rem;
        }
        .alert-label, .timeline-time {
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .alert-title, .timeline-title {
            font-size: 1rem;
            font-weight: 700;
            margin: 0.2rem 0 0.25rem;
        }
        .alert-meta, .timeline-detail {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.45;
        }
        .incident-card {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.03);
            margin-bottom: 0.85rem;
        }
        .incident-head {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-start;
            margin-bottom: 0.65rem;
        }
        .incident-title {
            font-size: 1.05rem;
            font-weight: 700;
        }
        .incident-meta {
            color: var(--muted);
            font-size: 0.85rem;
        }
        .incident-steps {
            margin: 0.7rem 0 0;
            padding-left: 1rem;
            color: var(--text);
        }
        .incident-steps li {
            margin-bottom: 0.35rem;
        }
        .sidebar-note {
            color: var(--muted);
            font-size: 0.85rem;
            line-height: 1.5;
        }
        @media (max-width: 980px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(snapshot) -> None:
    color = SEVERITY_STYLES.get(snapshot.rollup.highest_open_severity, "#57c7ff")
    st.markdown(
        f"""
        <section class="command-hero">
            <div class="eyebrow">Live Demo Fleet <span style="color:#9fb4ca;">Synthetic telemetry / 12-minute window</span></div>
            <div class="hero-grid">
                <div>
                    <h1 class="hero-title">AI Monitoring Command Center</h1>
                    <div class="hero-copy">
                        Monitor production-style AI operations signals across reliability, safety, latency, and budget pressure in one deliberately high-contrast command-center view.
                    </div>
                    <div class="hero-band">
                        <span class="hero-pill">Status: <strong style="color:{color}; margin-left:0.25rem;">{snapshot.rollup.overall_health_label}</strong></span>
                        <span class="hero-pill">Open incidents: <strong style="margin-left:0.25rem;">{snapshot.rollup.open_incidents}</strong></span>
                        <span class="hero-pill">Degraded services: <strong style="margin-left:0.25rem;">{snapshot.rollup.services_degraded}</strong></span>
                        <span class="hero-pill">Budget utilization: <strong style="margin-left:0.25rem;">{snapshot.rollup.budget_utilization:.0%}</strong></span>
                    </div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-label">Priority Condition</div>
                    <div class="hero-stat-value" style="color:{color};">{snapshot.rollup.highest_open_severity.upper()}</div>
                    <div class="hero-copy">
                        {snapshot.summary.headline}
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_rollup(snapshot) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monitored Services", len(snapshot.services), f"{snapshot.rollup.services_degraded} degraded")
    col2.metric("Active Alerts", len(snapshot.alerts), snapshot.rollup.highest_open_severity.upper())
    col3.metric("Spend Today", f"${snapshot.rollup.total_spend_today:,.0f}", f"{snapshot.rollup.budget_utilization:.0%} of budget")
    col4.metric("Avg Hallucination Risk", f"{snapshot.rollup.avg_hallucination_risk:.0%}", "fleet baseline")


def format_metric_value(value: float, unit: str) -> str:
    if unit == "%":
        return f"{value * 100:.1f}%"
    if unit == "$":
        return f"${value:,.0f}"
    return f"{value:.0f} {unit}"


def build_svg_chart(values: list[float], stroke: str, fill: str) -> str:
    width = 640
    height = 220
    left_pad = 18
    right_pad = 10
    top_pad = 18
    bottom_pad = 28
    if not values:
        return ""

    v_min = min(values)
    v_max = max(values)
    if math.isclose(v_min, v_max):
        v_min -= 1
        v_max += 1

    points: list[tuple[float, float]] = []
    for index, value in enumerate(values):
        x = left_pad + index * ((width - left_pad - right_pad) / max(len(values) - 1, 1))
        ratio = (value - v_min) / (v_max - v_min)
        y = top_pad + (1 - ratio) * (height - top_pad - bottom_pad)
        points.append((x, y))

    point_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area_points = f"{left_pad},{height-bottom_pad} {point_str} {points[-1][0]:.1f},{height-bottom_pad}"

    grid = []
    for step in range(4):
        y = top_pad + step * ((height - top_pad - bottom_pad) / 3)
        grid.append(
            f'<line x1="{left_pad}" y1="{y:.1f}" x2="{width-right_pad}" y2="{y:.1f}" '
            'stroke="rgba(159,180,202,0.18)" stroke-width="1" />'
        )

    labels = []
    for index in range(len(values)):
        x = left_pad + index * ((width - left_pad - right_pad) / max(len(values) - 1, 1))
        labels.append(
            f'<text x="{x:.1f}" y="{height-8}" text-anchor="middle" fill="#9fb4ca" '
            'font-size="11" font-family="Segoe UI, sans-serif">T-{}</text>'.format(len(values) - index - 1)
        )

    svg = f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="trend-fill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stop-color="{fill}" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="{fill}" stop-opacity="0.02"/>
            </linearGradient>
        </defs>
        {''.join(grid)}
        <polyline fill="url(#trend-fill)" points="{area_points}" />
        <polyline fill="none" stroke="{stroke}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" points="{point_str}" />
        {''.join(labels)}
    </svg>
    """
    return svg


def render_signal_panel(snapshot) -> None:
    trend_map = {trend.service_name: trend for trend in snapshot.trends}
    service_name = st.selectbox("Service", list(trend_map), index=0)
    metric_label = st.selectbox("Signal", list(METRIC_OPTIONS), index=0)
    attr_name, unit = METRIC_OPTIONS[metric_label]
    trend = trend_map[service_name]
    values = getattr(trend, attr_name)
    color = "#57c7ff" if metric_label in {"Latency p95", "Hourly Spend"} else "#ffd166"
    if metric_label == "Hallucination Risk":
        color = "#ff9a3c"
    if metric_label == "Error Rate":
        color = "#ff5d73"

    latest_value = values[-1]
    previous_value = values[-2]
    delta = latest_value - previous_value
    delta_label = format_metric_value(abs(delta), unit)
    direction = "up" if delta >= 0 else "down"

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-title">
            <div>
                <div class="panel-kicker">Signals</div>
                <h3 style="margin:0.15rem 0 0;">Operational Trend Explorer</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="chart-shell">
            <div class="chart-caption">
                <span>{html.escape(service_name)} · {html.escape(metric_label)}</span>
                <span>Latest: {format_metric_value(latest_value, unit)}</span>
            </div>
            {build_svg_chart(values, color, color)}
            <div class="chart-meta">
                <span>Change vs prior window: {direction} {delta_label}</span>
                <span>Observation points: {len(values)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_summary_panel(snapshot) -> None:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel-title">
            <div>
                <div class="panel-kicker">Command Brief</div>
                <h3 style="margin:0.15rem 0 0;">Operator Recommendations</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="summary-line">{html.escape(snapshot.summary.headline)}</div>', unsafe_allow_html=True)
    for index, item in enumerate(snapshot.summary.recommendations, start=1):
        st.markdown(
            f"""
            <div class="recommendation">
                <div class="recommendation-index">{index}</div>
                <div>{html.escape(item)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_service_matrix(snapshot) -> None:
    st.markdown("### Service Matrix")
    cols = st.columns(2)
    for index, service in enumerate(snapshot.services):
        with cols[index % 2]:
            status_color = STATUS_STYLES.get(service.status, "#57c7ff")
            st.markdown(
                f"""
                <div class="service-card">
                    <div class="service-top">
                        <div>
                            <div class="service-name">{html.escape(service.name)}</div>
                            <div class="service-owner">{html.escape(service.owner)}</div>
                        </div>
                        <div class="status-chip" style="color:{status_color}; background:rgba(255,255,255,0.04);">
                            {html.escape(service.status_label)}
                        </div>
                    </div>
                    {render_metric_bar('Latency p95', service.latency_p95_ms / 2000, f'{service.latency_p95_ms} ms', '#57c7ff')}
                    {render_metric_bar('Error rate', service.error_rate / 0.08, f'{service.error_rate * 100:.1f}%', '#ff5d73')}
                    {render_metric_bar('Hallucination risk', service.hallucination_risk / 0.25, f'{service.hallucination_risk * 100:.0f}%', '#ff9a3c')}
                    {render_metric_bar('Budget use', (service.spend_today_usd / service.daily_budget_usd), f'{service.spend_today_usd / service.daily_budget_usd:.0%}', '#ffd166')}
                    <div class="service-note">{html.escape(service.note)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_metric_bar(label: str, ratio: float, value: str, color: str) -> str:
    safe_ratio = max(0.0, min(ratio, 1.0))
    width = safe_ratio * 100
    return f"""
        <div class="service-metric">
            <div class="service-metric-head">
                <span>{html.escape(label)}</span>
                <span>{html.escape(value)}</span>
            </div>
            <div class="metric-bar">
                <div class="metric-fill" style="width:{width:.1f}%; background:{color};"></div>
            </div>
        </div>
    """


def render_alert_stack(snapshot) -> None:
    st.markdown("### Alert Stack")
    for alert in snapshot.alerts:
        color = SEVERITY_STYLES.get(alert.severity, "#57c7ff")
        st.markdown(
            f"""
            <div class="alert-card" style="border-left:4px solid {color};">
                <div class="alert-label" style="color:{color};">{alert.severity.upper()} · {html.escape(alert.service_name)}</div>
                <div class="alert-title">{html.escape(alert.title)}</div>
                <div class="alert-meta">{html.escape(alert.description)}</div>
                <div class="alert-meta" style="margin-top:0.35rem;">{html.escape(alert.metric_name)}: {html.escape(alert.current_value)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_timeline(snapshot) -> None:
    st.markdown("### Event Timeline")
    for event in snapshot.timeline:
        color = SEVERITY_STYLES.get(event.severity, "#57c7ff")
        st.markdown(
            f"""
            <div class="timeline-card" style="border-left:4px solid {color};">
                <div class="timeline-time" style="color:{color};">{html.escape(event.time_label)} · {event.severity.upper()}</div>
                <div class="timeline-title">{html.escape(event.title)}</div>
                <div class="timeline-detail">{html.escape(event.detail)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_incidents(snapshot) -> None:
    st.markdown("### Incident Board")
    for incident in snapshot.incidents:
        color = SEVERITY_STYLES.get(incident.severity, "#57c7ff")
        impacted = ", ".join(incident.impacted_services)
        steps = "".join(f"<li>{html.escape(step)}</li>" for step in incident.mitigation_steps)
        st.markdown(
            f"""
            <div class="incident-card">
                <div class="incident-head">
                    <div>
                        <div class="incident-title">{html.escape(incident.title)}</div>
                        <div class="incident-meta">{html.escape(incident.summary)}</div>
                    </div>
                    <div class="status-chip" style="color:{color}; background:rgba(255,255,255,0.04);">
                        {incident.severity.upper()} · {html.escape(incident.status_label)}
                    </div>
                </div>
                <div class="incident-meta">Commander: {html.escape(incident.commander)}</div>
                <div class="incident-meta">Impacted services: {html.escape(impacted)}</div>
                <ul class="incident-steps">{steps}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(page_title="AI Monitoring Command Center", layout="wide")
    inject_css()
    snapshot = build_demo_snapshot()

    with st.sidebar:
        st.markdown("## Control Room")
        st.markdown(
            '<div class="sidebar-note">Synthetic telemetry is fixed for the demo. Use the trend explorer to switch services and inspect reliability, safety, and cost movement.</div>',
            unsafe_allow_html=True,
        )
        st.metric("Critical alerts", sum(1 for alert in snapshot.alerts if alert.severity == "critical"))
        st.metric("High alerts", sum(1 for alert in snapshot.alerts if alert.severity == "high"))
        st.metric("Incident commanders", len({incident.commander for incident in snapshot.incidents}))

    render_hero(snapshot)
    st.write("")
    render_rollup(snapshot)
    st.write("")

    top_left, top_right = st.columns([1.45, 1])
    with top_left:
        render_signal_panel(snapshot)
    with top_right:
        render_summary_panel(snapshot)

    bottom_left, bottom_right = st.columns([1.2, 1])
    with bottom_left:
        render_service_matrix(snapshot)
        render_incidents(snapshot)
    with bottom_right:
        render_alert_stack(snapshot)
        render_timeline(snapshot)


if __name__ == "__main__":
    main()
