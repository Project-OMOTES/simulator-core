set profile_results_file=profiling_result.prof
set esdl_file=.\testdata\test1.esdl

pushd .
cd /D "%~dp0"

cd ..\..\
call .\venv\Scripts\activate
set PYTHONPATH=.\src\;%$PYTHONPATH%
python .\src\omotes_simulator_core\infrastructure\profiling.py %esdl_file% %profile_results_file%
start cmd /k snakeviz %profile_results_file%
popd