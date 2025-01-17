#!/usr/bin/env bash

if [[ "$OSTYPE" != "win32" && "$OSTYPE" != "msys" ]]; then
  echo "Activating .venv first."
  . .venv/bin/activate
fi

PYTHONPATH='$PYTHONPATH:src/' pytest -p no:faulthandler --junit-xml=test-results.xml unit_test/
