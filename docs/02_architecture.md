# AI Monitoring Command Center Architecture

## Overview

The project is intentionally small and portfolio-friendly: a Streamlit frontend renders a synthetic monitoring snapshot assembled from in-repo Python modules. The goal is to show product thinking around AI operations rather than infrastructure complexity.

## Components

- `app/app.py`
  - Presentation layer for the command-center dashboard
  - Renders fleet health, service metrics, alerts, and incidents
- `src/project/monitoring/demo_data.py`
  - Defines a realistic demo scenario for monitored AI services
- `src/project/monitoring/rules.py`
  - Converts raw service metrics into operator-facing alerts
- `src/project/monitoring/summary.py`
  - Produces fleet rollups and concise recommendations
- `src/project/monitoring/service.py`
  - Orchestrates the snapshot assembly used by the UI and tests
- `scripts/export_snapshot.py`
  - Exports a static monitoring snapshot artifact for review or handoff

## Data Flow

1. Load synthetic service and incident data.
2. Evaluate alert rules against the service metrics.
3. Build fleet-level rollups from the service, alert, and incident sets.
4. Generate an executive summary and recommendations.
5. Render the snapshot in Streamlit or export it as JSON.

## Design Principles

- Deterministic demo behavior
  - The dataset and alert rules are static so portfolio reviewers see a stable scenario.
- Small, testable domain layer
  - Monitoring logic lives in plain Python modules rather than being buried in the UI.
- Clear separation between data, rules, and presentation
  - This keeps future upgrades like live telemetry or persistence straightforward.

## Future Extension Points

- Add time-series history and trend charts
- Persist snapshots, alerts, and incident changes
- Introduce environment and owner filtering
- Replace synthetic data with local files or mock API ingestion
