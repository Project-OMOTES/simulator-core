pushd .
cd /D "%~dp0"
cd ..\..\
call .\venv\Scripts\activate
python .\src\simulator_core\infrastructure\profile_test.py
snakeviz .\src\simulator_core\infrastructure\results.prof
popd 