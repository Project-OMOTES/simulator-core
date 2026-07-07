@echo on

rem Jump to the directory where this build.cmd script is
cd /d %~dp0

py -3.11 -m venv .\venv
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
rem Install the package in editable mode
cd ..
pip install -e .
rem Jump back to the directory where this build.cmd script is
cd /d %~dp0
call .\venv\Scripts\deactivate.bat