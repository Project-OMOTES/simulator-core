rem Short script to run linting
rem @echo off
set PYTHONUTF8=1
pushd .
cd /D "%~dp0"
cd ..\..\
flake8 ./src/omotes_simulator_core ./unit_test/
popd
