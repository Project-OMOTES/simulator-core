rem Short script to run linting
rem @echo off

pushd .
cd /D "%~dp0"
cd ..\..\
black --check --diff ./src/omotes_simulator_core ./unit_test/ --exclude __init__.py
isort --check-only --diff ./src/omotes_simulator_core ./unit_test/ --skip __init__.py
popd
