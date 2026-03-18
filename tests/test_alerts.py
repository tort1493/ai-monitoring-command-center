from project.monitoring.demo_data import load_demo_services
from project.monitoring.rules import evaluate_alerts


def test_alerts_include_expected_critical_and_high_conditions() -> None:
    alerts = evaluate_alerts(load_demo_services())
    titles = {(alert.service_name, alert.title, alert.severity) for alert in alerts}

    assert ("Inference Gateway", "Latency SLO breach", "high") in titles
    assert ("Inference Gateway", "Error rate escalation", "critical") in titles
    assert ("Support Copilot", "Hallucination risk drift", "high") in titles
    assert ("Safety Moderation", "Moderation drift detected", "critical") in titles


def test_alerts_are_sorted_by_severity() -> None:
    alerts = evaluate_alerts(load_demo_services())

    severities = [alert.severity for alert in alerts]
    assert severities[:2] == ["critical", "critical"]
