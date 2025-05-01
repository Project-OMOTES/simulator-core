#!/usr/bin/env bash

if [[ "$OSTYPE" != "win32" && "$OSTYPE" != "msys" ]]; then
  echo "Activating .venv first."
  . .venv/bin/activate
fi

black --check --diff ./src/omotes_simulator_core ./unit_test/ --exclude __init__.py
isort --check-only --diff ./src/omotes_simulator_core ./unit_test/ --skip __init__.py

