from __future__ import annotations

from project.monitoring.models import Alert, ServiceStatus


def evaluate_alerts(services: list[ServiceStatus]) -> list[Alert]:
    alerts: list[Alert] = []

    for service in services:
        if service.latency_p95_ms >= 1500:
            alerts.append(
                Alert(
                    severity="high",
                    service_name=service.name,
                    title="Latency SLO breach",
                    description="Tail latency exceeded the 1.5s threshold for the active observation window.",
                    metric_name="latency_p95_ms",
                    current_value=f"{service.latency_p95_ms} ms",
                )
            )

        if service.error_rate >= 0.05:
            alerts.append(
                Alert(
                    severity="critical",
                    service_name=service.name,
                    title="Error rate escalation",
                    description="Request failures crossed the 5% escalation threshold.",
                    metric_name="error_rate",
                    current_value=f"{service.error_rate * 100:.1f}%",
                )
            )

        if service.hallucination_risk >= 0.18:
            alerts.append(
                Alert(
                    severity="high",
                    service_name=service.name,
                    title="Hallucination risk drift",
                    description="Evaluator and QA signals indicate response grounding quality is deteriorating.",
                    metric_name="hallucination_risk",
                    current_value=f"{service.hallucination_risk * 100:.0f}%",
                )
            )

        if service.moderation_drift >= 0.08:
            alerts.append(
                Alert(
                    severity="critical",
                    service_name=service.name,
                    title="Moderation drift detected",
                    description="Safety performance has deviated materially from the established baseline.",
                    metric_name="moderation_drift",
                    current_value=f"{service.moderation_drift * 100:.0f} pts",
                )
            )

        budget_utilization = service.spend_today_usd / service.daily_budget_usd
        if budget_utilization >= 0.9:
            alerts.append(
                Alert(
                    severity="medium",
                    service_name=service.name,
                    title="Budget pressure",
                    description="Daily spend is approaching or exceeding the configured budget ceiling.",
                    metric_name="budget_utilization",
                    current_value=f"{budget_utilization:.0%}",
                )
            )

    return sort_alerts(alerts)


def sort_alerts(alerts: list[Alert]) -> list[Alert]:
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(alerts, key=lambda alert: (severity_rank.get(alert.severity, 99), alert.service_name, alert.title))
