#!/usr/bin/env bash

python3 -m venv ./.venv
if [[ "$OSTYPE" != "win32" && "$OSTYPE" != "msys" ]]; then
  echo "Activating .venv first."
  . .venv/bin/activate
fi

pip3 install pip-tools
./ci/linux/update_dependencies.sh
./ci/linux/install_dependencies.sh
