#!/usr/bin/env sh

. .venv/bin/activate
python -m piptools sync  ./requirements.txt ./dev-requirements.txt
