#!/usr/bin/env bash

if [[ "$OSTYPE" != "win32" && "$OSTYPE" != "msys" ]]; then
  echo "Activating .venv first."
  . .venv/bin/activate
fi

black ./src/omotes_simulator_core ./unit_test/
isort --diff ./src/omotes_simulator_core ./unit_test/

