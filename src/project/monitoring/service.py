from __future__ import annotations

from project.monitoring.demo_data import load_demo_incidents, load_demo_services
from project.monitoring.models import MonitoringSnapshot
from project.monitoring.rules import evaluate_alerts
from project.monitoring.summary import build_rollup, build_summary


def build_demo_snapshot() -> MonitoringSnapshot:
    services = load_demo_services()
    incidents = load_demo_incidents()
    alerts = evaluate_alerts(services)
    rollup = build_rollup(services, alerts, incidents)
    summary = build_summary(services, alerts, incidents, rollup)
    return MonitoringSnapshot(
        services=services,
        alerts=alerts,
        incidents=incidents,
        rollup=rollup,
        summary=summary,
    )
