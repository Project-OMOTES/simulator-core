
pushd .
cd /D "%~dp0"
pip-compile --upgrade --output-file=..\..\requirements.txt ..\..\pyproject.toml
pip-compile --upgrade --extra=dev --output-file=..\..\dev-requirements.txt -c ..\..\requirements.txt ..\..\pyproject.toml
popd