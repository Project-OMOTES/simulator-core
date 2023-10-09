
pushd .
cd /D "%~dp0"
cd ..\..\
pip-sync .\requirements.txt .\dev-requirements.txt
popd