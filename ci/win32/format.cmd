rem Short script to run formatting
rem @echo off

pushd .
cd /D "%~dp0"
cd ..\..\
black ./src/omotes_simulator_core
isort ./src/omotes_simulator_core
popd
