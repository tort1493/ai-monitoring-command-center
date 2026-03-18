from __future__ import annotations

from project.monitoring.models import Incident, ServiceStatus


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
