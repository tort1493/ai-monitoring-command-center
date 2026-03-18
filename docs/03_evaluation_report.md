# AI Monitoring Command Center Roadmap

## Current MVP

The current version is a deterministic command-center demo with:

- Synthetic service health signals
- Rule-based alert generation
- Incident tracking
- Fleet rollups and operator recommendations
- Streamlit presentation layer

## Gaps Before Production-Style Depth

- No persisted telemetry history yet
- No real event ingestion from model gateways, tracing, or evaluator jobs
- No authentication, RBAC, or multi-team workspace model
- No acknowledgement workflow for alerts

## Next Build Phases

1. Add snapshot history and time-series charts for latency, spend, and safety metrics.
2. Ingest structured JSON events from local files or a mock API.
3. Add alert acknowledgement, incident state transitions, and owner filters.
4. Introduce model-version comparisons to detect regressions after rollout.

## Portfolio Story

This project is designed to demonstrate that AI products need more than model integration. They need observability, drift detection, budget monitoring, and incident operations that product and platform teams can actually use.
