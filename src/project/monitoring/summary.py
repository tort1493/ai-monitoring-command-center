from __future__ import annotations

from project.monitoring.models import Alert, FleetRollup, Incident, ServiceStatus, SummaryCard


def build_rollup(
    services: list[ServiceStatus], alerts: list[Alert], incidents: list[Incident]
) -> FleetRollup:
    total_spend = sum(service.spend_today_usd for service in services)
    total_budget = sum(service.daily_budget_usd for service in services)
    degraded = sum(1 for service in services if service.status != "healthy")
    avg_hallucination_risk = sum(service.hallucination_risk for service in services) / len(services)

    highest_open_severity = "low"
    if any(alert.severity == "critical" for alert in alerts):
        highest_open_severity = "critical"
        health = "Critical Attention Required"
    elif any(alert.severity == "high" for alert in alerts):
        highest_open_severity = "high"
        health = "Degraded"
    elif alerts:
        highest_open_severity = "medium"
        health = "Watch"
    else:
        health = "Healthy"

    return FleetRollup(
        total_spend_today=total_spend,
        budget_utilization=total_spend / total_budget,
        avg_hallucination_risk=avg_hallucination_risk,
        services_degraded=degraded,
        open_incidents=len([incident for incident in incidents if incident.status != "resolved"]),
        highest_open_severity=highest_open_severity,
        overall_health_label=health,
    )


def build_summary(
    services: list[ServiceStatus], alerts: list[Alert], incidents: list[Incident], rollup: FleetRollup
) -> SummaryCard:
    highest_latency = max(services, key=lambda service: service.latency_p95_ms)
    highest_risk = max(services, key=lambda service: service.hallucination_risk)
    active_incident = next((incident for incident in incidents if incident.status != "resolved"), None)

    headline = (
        f"{rollup.overall_health_label}: {rollup.open_incidents} open incident(s) and "
        f"{len(alerts)} active alert(s) across {len(services)} monitored AI services."
    )

    recommendations = [
        f"Stabilize {highest_latency.name} first; it has the worst tail latency at {highest_latency.latency_p95_ms} ms.",
        f"Re-run grounding and regression checks for {highest_risk.name}; hallucination risk is {highest_risk.hallucination_risk:.0%}.",
        f"Control spend immediately; fleet budget utilization is {rollup.budget_utilization:.0%} for the day.",
    ]
    if active_incident:
        recommendations.insert(
            0,
            f"Keep incident command with {active_incident.commander} until {active_incident.title.lower()} is downgraded.",
        )

    return SummaryCard(headline=headline, recommendations=recommendations)
