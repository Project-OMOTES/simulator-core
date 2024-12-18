#!/usr/bin/env bash

if [[ "$OSTYPE" != "win32" && "$OSTYPE" != "msys" ]]; then
  echo "Activating .venv first."
  . .venv/bin/activate
fi

pip-compile --upgrade --output-file=requirements.txt pyproject.toml
pip-compile --upgrade --extra=dev --output-file=dev-requirements.txt -c requirements.txt pyproject.toml
