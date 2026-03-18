from __future__ import annotations

from project.monitoring.demo_data import (
    load_demo_incidents,
    load_demo_services,
    load_demo_timeline,
    load_demo_trends,
)
from project.monitoring.models import MonitoringSnapshot
from project.monitoring.rules import evaluate_alerts
from project.monitoring.summary import build_rollup, build_summary


def build_demo_snapshot() -> MonitoringSnapshot:
    services = load_demo_services()
    incidents = load_demo_incidents()
    trends = load_demo_trends()
    timeline = load_demo_timeline()
    alerts = evaluate_alerts(services)
    rollup = build_rollup(services, alerts, incidents)
    summary = build_summary(services, alerts, incidents, rollup)
    return MonitoringSnapshot(
        services=services,
        alerts=alerts,
        incidents=incidents,
        trends=trends,
        timeline=timeline,
        rollup=rollup,
        summary=summary,
    )
