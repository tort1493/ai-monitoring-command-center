from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServiceStatus:
    name: str
    owner: str
    status: str
    latency_p95_ms: int
    error_rate: float
    hallucination_risk: float
    moderation_drift: float
    spend_today_usd: float
    daily_budget_usd: float
    note: str

    @property
    def status_label(self) -> str:
        return self.status.replace("_", " ").title()


@dataclass(frozen=True)
class Alert:
    severity: str
    service_name: str
    title: str
    description: str
    metric_name: str
    current_value: str


@dataclass(frozen=True)
class Incident:
    title: str
    severity: str
    status: str
    summary: str
    commander: str
    impacted_services: list[str]
    mitigation_steps: list[str]

    @property
    def status_label(self) -> str:
        return self.status.replace("_", " ").title()


@dataclass(frozen=True)
class FleetRollup:
    total_spend_today: float
    budget_utilization: float
    avg_hallucination_risk: float
    services_degraded: int
    open_incidents: int
    highest_open_severity: str
    overall_health_label: str


@dataclass(frozen=True)
class ServiceTrend:
    service_name: str
    latency_p95_ms: list[int]
    error_rate: list[float]
    hallucination_risk: list[float]
    spend_hourly_usd: list[float]


@dataclass(frozen=True)
class TimelineEvent:
    time_label: str
    severity: str
    title: str
    detail: str


@dataclass(frozen=True)
class SummaryCard:
    headline: str
    recommendations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MonitoringSnapshot:
    services: list[ServiceStatus]
    alerts: list[Alert]
    incidents: list[Incident]
    trends: list[ServiceTrend]
    timeline: list[TimelineEvent]
    rollup: FleetRollup
    summary: SummaryCard
