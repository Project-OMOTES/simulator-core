rem Short script to initialize virtual environment using venv and pip
rem @echo off

pushd .
cd /D "%~dp0"

set VENV_DIR=..\..\venv

py --list | findstr /i /C:"3.11" 
if %errorlevel% == 0 (
    echo Python 3.11 found!
    py -3.11 -m venv %VENV_DIR%
) else (
    echo Python 3.11 not found, using installed 3.X
    py -3 -m venv %VENV_DIR%
    echo Python version is:
    py -3 --version
)

if not exist %VENV_DIR%\Scripts\activate.bat (
    echo Virtual environment not created successfully.
    exit /b 1
)
if not exist %VENV_DIR%\Scripts\python.exe (
    echo Python executable not found in the virtual environment.
    echo Dependencies are not installed!
    exit /b 1
)

call %VENV_DIR%\Scripts\activate.bat
python -m ensurepip --upgrade
python -m pip install pip-tools setuptools wheel
call .\install_dependencies.cmd
call .\install_dev.cmd
call .\check_java_jdk.cmd
popd
