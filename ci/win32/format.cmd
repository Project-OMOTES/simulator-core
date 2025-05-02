rem Short script to run linting
rem @echo off

pushd .
cd /D "%~dp0"
cd ..\..\
black ./src/omotes_simulator_core ./unit_test/
isort --diff ./src/omotes_simulator_core ./unit_test/
popd
