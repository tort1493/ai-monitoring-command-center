from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from project.monitoring.service import build_demo_snapshot


SEVERITY_STYLES = {
    "critical": "#ef4444",
    "high": "#f97316",
    "medium": "#eab308",
    "low": "#38bdf8",
}


def render_header(snapshot) -> None:
    st.title("AI Monitoring Command Center")
    st.caption(
        "Synthetic command-center view for model reliability, safety drift, and incident response."
    )

    health = snapshot.rollup.overall_health_label
    color = SEVERITY_STYLES.get(snapshot.rollup.highest_open_severity, "#38bdf8")
    st.markdown(
        f"""
        <div style="padding: 1rem 1.2rem; border: 1px solid #1f2937; border-radius: 18px;
        background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(17,24,39,0.84));
        margin-bottom: 1rem;">
            <div style="font-size: 0.85rem; color: #94a3b8;">Fleet Status</div>
            <div style="font-size: 2rem; font-weight: 700; color: {color};">{health}</div>
            <div style="font-size: 0.95rem; color: #cbd5e1;">
                {snapshot.rollup.services_degraded} degraded service(s),
                {snapshot.rollup.open_incidents} open incident(s),
                ${snapshot.rollup.total_spend_today:,.0f} spend today
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_rollup(snapshot) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Services", len(snapshot.services), f"{snapshot.rollup.services_degraded} degraded")
    col2.metric("Open Alerts", len(snapshot.alerts), snapshot.rollup.highest_open_severity.upper())
    col3.metric("Spend Today", f"${snapshot.rollup.total_spend_today:,.0f}", f"{snapshot.rollup.budget_utilization:.0%} of budget")
    col4.metric("Avg Hallucination Risk", f"{snapshot.rollup.avg_hallucination_risk:.0%}", snapshot.rollup.overall_health_label)


def render_summary(snapshot) -> None:
    st.subheader("Command Summary")
    st.write(snapshot.summary.headline)
    for item in snapshot.summary.recommendations:
        st.markdown(f"- {item}")


def render_services(snapshot) -> None:
    st.subheader("Service Grid")
    for service in snapshot.services:
        with st.container(border=True):
            cols = st.columns([2, 1, 1, 1, 1, 1])
            cols[0].markdown(f"**{service.name}**  \n{service.owner}")
            cols[1].metric("Status", service.status_label)
            cols[2].metric("Latency p95", f"{service.latency_p95_ms} ms")
            cols[3].metric("Error Rate", f"{service.error_rate * 100:.1f}%")
            cols[4].metric("Hallucination", f"{service.hallucination_risk * 100:.0f}%")
            cols[5].metric("Spend", f"${service.spend_today_usd:,.0f}")
            st.caption(service.note)


def render_alerts(snapshot) -> None:
    st.subheader("Active Alerts")
    if not snapshot.alerts:
        st.info("No active alerts.")
        return
    for alert in snapshot.alerts:
        color = SEVERITY_STYLES.get(alert.severity, "#38bdf8")
        st.markdown(
            f"""
            <div style="padding: 0.8rem 1rem; border-left: 5px solid {color};
            background: rgba(15, 23, 42, 0.55); margin-bottom: 0.75rem; border-radius: 8px;">
                <div style="font-weight: 700;">[{alert.severity.upper()}] {alert.title}</div>
                <div style="color: #cbd5e1;">{alert.description}</div>
                <div style="font-size: 0.85rem; color: #94a3b8;">{alert.service_name} | {alert.metric_name}: {alert.current_value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_incidents(snapshot) -> None:
    st.subheader("Incident Feed")
    for incident in snapshot.incidents:
        with st.expander(f"{incident.severity.upper()} | {incident.title}", expanded=incident.status != "resolved"):
            st.write(incident.summary)
            st.write(f"Status: {incident.status_label}")
            st.write(f"Impacted services: {', '.join(incident.impacted_services)}")
            st.write(f"Commander: {incident.commander}")
            st.write("Mitigation steps:")
            for step in incident.mitigation_steps:
                st.markdown(f"- {step}")


def main() -> None:
    st.set_page_config(page_title="AI Monitoring Command Center", layout="wide")
    snapshot = build_demo_snapshot()

    render_header(snapshot)
    render_rollup(snapshot)

    left, right = st.columns([1.2, 1])
    with left:
        render_services(snapshot)
        render_incidents(snapshot)
    with right:
        render_summary(snapshot)
        render_alerts(snapshot)


if __name__ == "__main__":
    main()
