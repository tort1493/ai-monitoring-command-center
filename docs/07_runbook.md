# AI Monitoring Command Center Runbook

## Purpose

Operate the AI Monitoring Command Center in local and demo settings, validate that the dashboard reflects the expected synthetic fleet state, and define the response path when monitoring signals look inconsistent.

## Local Run

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Test

```bash
pytest
```

## Snapshot Export

```bash
python scripts/export_snapshot.py
```

## Demo Narrative

Use the dashboard to walk through three common AI-ops failure modes:

1. Tail-latency pressure on shared inference infrastructure
2. Hallucination drift in a customer-facing copilot
3. Moderation regression after a provider model version change

## Normal Operating Procedure

1. Launch the Streamlit app and confirm the dashboard loads without import errors.
2. Verify the fleet header shows a degraded or critical state for the current demo dataset.
3. Check that active alerts include latency, hallucination, moderation, and budget signals.
4. Open the incident feed and confirm the mitigation steps are visible for each active incident.
5. Export a snapshot when you need a static artifact for review or handoff.

## Alert Symptoms

- Dashboard fails to render the service grid or incident feed
- Expected alerts do not appear for clearly degraded services
- Summary recommendations do not reflect the highest-risk services
- Exported snapshot is missing services, incidents, or rollup fields

## Incident Steps

1. Re-run the app locally to rule out a transient runtime issue.
2. Export a fresh snapshot with `python scripts/export_snapshot.py`.
3. Compare the exported snapshot with the values shown in the dashboard.
4. Inspect alert rules and summary logic for threshold or aggregation regressions.
5. Update tests first if the intended fleet behavior changed.

## Recovery Actions

- Restore the synthetic dataset if the demo scenario was edited unintentionally.
- Adjust alert thresholds only when the resulting operator behavior is clearly better.
- Keep summary recommendations tied to the highest-latency and highest-risk services.
- Regenerate the snapshot artifact after any monitoring logic change.

## Ownership

- Product/demo owner: repository maintainer
- Technical owner for monitoring logic: repository maintainer
- Incident reviewer: repository maintainer until a broader team exists
