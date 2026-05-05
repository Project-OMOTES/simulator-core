@echo on
setlocal

rem Jump to the directory where this script is located (doc\)
pushd "%~dp0"

set "PY_BOOTSTRAP=python"
where py >NUL 2>NUL
if %ERRORLEVEL% EQU 0 set "PY_BOOTSTRAP=py"

if not exist .\venv\Scripts\python.exe (
    echo Creating virtual environment...
    %PY_BOOTSTRAP% -m venv .\venv

    call .\venv\Scripts\activate.bat
) else (
    echo Using existing virtual environment...
    call .\venv\Scripts\activate.bat
)

python -m pip install -r requirements.txt

call make.bat clean
call make.bat html


call .\venv\Scripts\deactivate.bat
popd
endlocal
pause
