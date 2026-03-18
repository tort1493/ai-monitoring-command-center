from __future__ import annotations

from project.monitoring.models import Incident, ServiceStatus, ServiceTrend, TimelineEvent


def load_demo_services() -> list[ServiceStatus]:
    return [
        ServiceStatus(
            name="Inference Gateway",
            owner="Platform Ops",
            status="degraded",
            latency_p95_ms=1890,
            error_rate=0.061,
            hallucination_risk=0.08,
            moderation_drift=0.01,
            spend_today_usd=3820.0,
            daily_budget_usd=5000.0,
            note="Traffic surge from evaluation batch workloads is saturating the primary gateway.",
        ),
        ServiceStatus(
            name="Support Copilot",
            owner="CX Engineering",
            status="degraded",
            latency_p95_ms=1240,
            error_rate=0.024,
            hallucination_risk=0.21,
            moderation_drift=0.04,
            spend_today_usd=2140.0,
            daily_budget_usd=2500.0,
            note="Hallucination checks are drifting upward after the latest prompt package rollout.",
        ),
        ServiceStatus(
            name="Document Extraction",
            owner="Knowledge Systems",
            status="healthy",
            latency_p95_ms=620,
            error_rate=0.008,
            hallucination_risk=0.03,
            moderation_drift=0.0,
            spend_today_usd=910.0,
            daily_budget_usd=1800.0,
            note="OCR and extraction throughput remain within the expected operating band.",
        ),
        ServiceStatus(
            name="Safety Moderation",
            owner="Trust Engineering",
            status="incident",
            latency_p95_ms=710,
            error_rate=0.017,
            hallucination_risk=0.05,
            moderation_drift=0.11,
            spend_today_usd=1650.0,
            daily_budget_usd=1600.0,
            note="False-negative rate increased after provider model version rotation.",
        ),
    ]


def load_demo_incidents() -> list[Incident]:
    return [
        Incident(
            title="Moderation false-negative spike",
            severity="critical",
            status="mitigating",
            summary="Safety moderation is missing policy-violating prompts above the normal baseline. The team has shifted high-risk routes to a fallback policy stack.",
            commander="Riley Chen",
            impacted_services=["Safety Moderation", "Support Copilot"],
            mitigation_steps=[
                "Route high-risk traffic to fallback moderation policy.",
                "Increase manual review sample size for newly flagged sessions.",
                "Block automatic provider version adoption until regression suite passes.",
            ],
        ),
        Incident(
            title="Inference queue saturation",
            severity="high",
            status="investigating",
            summary="The shared inference gateway is hitting a queue backlog during evaluation bursts, increasing tail latency for customer-facing traffic.",
            commander="Avery Patel",
            impacted_services=["Inference Gateway"],
            mitigation_steps=[
                "Throttle non-critical batch evaluations.",
                "Shift latency-sensitive traffic to the standby region.",
            ],
        ),
    ]


def load_demo_trends() -> list[ServiceTrend]:
    return [
        ServiceTrend(
            service_name="Inference Gateway",
            latency_p95_ms=[920, 980, 1040, 1210, 1360, 1480, 1620, 1890],
            error_rate=[0.012, 0.015, 0.019, 0.024, 0.031, 0.038, 0.049, 0.061],
            hallucination_risk=[0.04, 0.04, 0.05, 0.05, 0.06, 0.07, 0.07, 0.08],
            spend_hourly_usd=[270, 290, 310, 340, 395, 430, 470, 520],
        ),
        ServiceTrend(
            service_name="Support Copilot",
            latency_p95_ms=[810, 840, 890, 940, 1010, 1090, 1160, 1240],
            error_rate=[0.010, 0.011, 0.013, 0.016, 0.018, 0.020, 0.022, 0.024],
            hallucination_risk=[0.09, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.21],
            spend_hourly_usd=[180, 205, 230, 245, 268, 295, 320, 350],
        ),
        ServiceTrend(
            service_name="Document Extraction",
            latency_p95_ms=[590, 610, 605, 615, 630, 625, 618, 620],
            error_rate=[0.011, 0.010, 0.009, 0.009, 0.008, 0.008, 0.008, 0.008],
            hallucination_risk=[0.04, 0.04, 0.04, 0.03, 0.03, 0.03, 0.03, 0.03],
            spend_hourly_usd=[92, 99, 108, 116, 121, 123, 126, 125],
        ),
        ServiceTrend(
            service_name="Safety Moderation",
            latency_p95_ms=[540, 560, 575, 610, 640, 670, 690, 710],
            error_rate=[0.008, 0.009, 0.010, 0.012, 0.013, 0.015, 0.016, 0.017],
            hallucination_risk=[0.03, 0.03, 0.03, 0.04, 0.04, 0.04, 0.05, 0.05],
            spend_hourly_usd=[150, 162, 175, 188, 201, 214, 223, 237],
        ),
    ]


def load_demo_timeline() -> list[TimelineEvent]:
    return [
        TimelineEvent(
            time_label="09:10",
            severity="medium",
            title="Grounding evaluator drift",
            detail="Support Copilot QA checks started missing expected citations after prompt package release 26.3.",
        ),
        TimelineEvent(
            time_label="10:25",
            severity="high",
            title="Inference queue backlog",
            detail="Batch evaluation traffic saturated shared gateway workers and pushed customer traffic into the tail-latency band.",
        ),
        TimelineEvent(
            time_label="11:40",
            severity="critical",
            title="Moderation regression confirmed",
            detail="Fallback safety stack enabled after false-negative rate moved outside the acceptable threshold.",
        ),
        TimelineEvent(
            time_label="12:05",
            severity="high",
            title="Regional traffic shift",
            detail="Latency-sensitive routes were diverted to standby capacity while the primary queue drains.",
        ),
    ]
