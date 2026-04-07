@echo off
cd /d "%~dp0"

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Instala dependencias se necessario
pip install -q -r requirements.txt

REM Roda o app
python main.py

pause
