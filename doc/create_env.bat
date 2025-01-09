@echo on

rem Jump to the directory where this build.cmd script is
cd /d %~dp0

python -m virtualenv venv
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
call .\venv\Scripts\deactivate.bat