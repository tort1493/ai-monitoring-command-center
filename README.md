# AI Monitoring Command Center

This project is a local-first Streamlit dashboard that simulates how an operations team monitors AI systems in production. It highlights model health, latency, cost, moderation drift, and active incidents in a single command-center view.

## Features

- Live-style command-center UI with service status, alerts, and incident feed
- Synthetic monitoring snapshot with realistic AI operations signals
- Rule-based alerting for latency, error rate, hallucination risk, moderation drift, and budget pressure
- Executive summary and operator recommendations generated from the current system state
- Lightweight pytest coverage for alerting and fleet rollups

## Quickstart

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the UI:

```bash
streamlit run app/app.py
```

4. Run tests:

```bash
pytest
```

## Project Layout

- `app/app.py`: Streamlit command-center interface
- `src/project/monitoring/`: monitoring models, synthetic data, alert logic, and summaries
- `tests/`: unit coverage for alerts and snapshot rollups
- `docs/`: architecture and operating notes for the portfolio project

## Monitoring Concepts

- `Latency p95`: tail latency for model and gateway services
- `Error rate`: failed request percentage over the latest observation window
- `Hallucination risk`: proxy score from evaluator runs and sampled QA checks
- `Moderation drift`: percentage-point change from baseline safety performance
- `Budget burn`: daily spend versus the configured daily budget
