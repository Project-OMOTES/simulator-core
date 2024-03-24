#!/usr/bin/env sh

. .venv/bin/activate
git reset --hard # Reset any changes made during the create_env
python -m build
