
pushd .
cd /D "%~dp0"

cd ..\..\
call .\venv\Scripts\activate
set PYTHONPATH=.\src\;%$PYTHONPATH%
pytest -p no:faulthandler unit_test/ 
popd