set profile_results_file=profiling_result_final.prof
set esdl_file="C:\Users\zwan\Downloads\Delft_TPCv_supply_only with return network.esdl"

pushd .
cd /D "%~dp0"

cd ..\..\
call .\.venv\Scripts\activate
set PYTHONPATH=.\src\;%$PYTHONPATH%
python .\src\omotes_simulator_core\infrastructure\profiling.py %esdl_file% %profile_results_file%
start cmd /k snakeviz %profile_results_file%
popd