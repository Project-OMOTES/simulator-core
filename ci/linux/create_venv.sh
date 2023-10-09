#!/usr/bin/env sh

python3.11 -m venv ./.venv
. .venv/bin/activate
pip3 install pip-tools
./ci/linux/update_dependencies.sh
./ci/linux/install_dependencies.sh
