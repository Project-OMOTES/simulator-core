#!/usr/bin/env sh

. .venv/bin/activate
git reset --hard  # reset any changes in git repo
python -m build
