#!/usr/bin/env bash

set -euo pipefail

# Jump to the directory where this script is located (doc/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "$SCRIPT_DIR" > /dev/null
cd ..

if [ ! -f "./.venv/bin/python" ]; then
	echo "Creating virtual environment..."
	if command -v python3 >/dev/null 2>&1; then
		python3 -m venv .venv
	elif command -v python >/dev/null 2>&1; then
		python -m venv .venv
	else
		echo "Error: python3 or python is required to create a virtual environment."
		popd > /dev/null
		exit 1
	fi
else
	echo "Using existing virtual environment..."
fi

# shellcheck source=/dev/null
source "./.venv/bin/activate"

cd ..
python -m pip install -r requirements.txt

make clean
make html

deactivate
popd > /dev/null
