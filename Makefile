.PHONY: setup lint test run export-snapshot docker-build docker-run

setup:
\tpython -m venv .venv
\tpython -m pip install -r requirements.txt

lint:
\truff check .
\tpython -m compileall src

test:
\tpytest -q

run:
\tstreamlit run app/app.py

export-snapshot:
\tpython scripts/export_snapshot.py

docker-build:
\tdocker build -t ai-monitoring-command-center .

docker-run:
\tdocker run -p 8501:8501 ai-monitoring-command-center
