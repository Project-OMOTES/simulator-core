
pushd .
cd /D "%~dp0"
cd ..\..\
python -m piptools sync
popd