rem Short script to initialize virtual environment using venv and pip
rem @echo off

pushd .
cd /D "%~dp0"

py --list | findstr /i /C:"3.11" 
if %errorlevel% == 0 (
    echo Python 3.11 found!.
    py -3.11 -m venv ..\..\venv
) else (
    echo Python 3.11 not found, using installed 3.X version.
    py -3 -m venv ..\..\venv
)

if not exist ..\..\venv\Scripts\activate.bat (
    echo Virtual environment not created successfully.
    exit /b 1
)
if not exist ..\..\venv\Scripts\python.exe (
    echo Python executable not found in the virtual environment.
    exit /b 1
)

call ..\..\venv\Scripts\activate.bat
python -m ensurepip --upgrade
python -m pip install pip-tools setuptools wheel
REM call .\update_dependencies.cmd
call .\install_dependencies.cmd
call .\install_dev.cmd
call .\check_java_jdk.cmd
popd
