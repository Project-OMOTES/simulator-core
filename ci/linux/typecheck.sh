#!/usr/bin/env sh

. .venv/bin/activate
python -m mypy ./src/simulator.core ./unit_test/
