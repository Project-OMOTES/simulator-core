#!/usr/bin/env sh

. .venv/bin/activate
pip-sync  ./requirements.txt ./dev-requirements.txt
