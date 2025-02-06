@echo on

rem Jump to the directory where this build.cmd script is
cd /d %~dp0

call .\venv\Scripts\activate.bat
cd ..
pip install -r requirements.txt
cd doc
call make.bat html
call .\venv\Scripts\deactivate.bat
pause