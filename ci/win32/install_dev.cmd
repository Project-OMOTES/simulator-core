
pushd .
cd /D "%~dp0"
cd ..\..\
python -m piptools sync .\requirements.txt .\dev-requirements.txt
popd