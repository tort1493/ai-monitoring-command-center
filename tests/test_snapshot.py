from project.monitoring.service import build_demo_snapshot


def test_snapshot_rollup_matches_demo_state() -> None:
    snapshot = build_demo_snapshot()

    assert snapshot.rollup.services_degraded == 3
    assert snapshot.rollup.open_incidents == 2
    assert snapshot.rollup.highest_open_severity == "critical"
    assert snapshot.rollup.overall_health_label == "Critical Attention Required"


def test_summary_contains_actionable_recommendations() -> None:
    snapshot = build_demo_snapshot()

    assert snapshot.summary.recommendations
    assert "incident command" in snapshot.summary.recommendations[0].lower()


def test_snapshot_includes_trends_and_timeline() -> None:
    snapshot = build_demo_snapshot()

    assert len(snapshot.trends) == len(snapshot.services)
    assert snapshot.timeline
    assert len(snapshot.trends[0].latency_p95_ms) == 8
