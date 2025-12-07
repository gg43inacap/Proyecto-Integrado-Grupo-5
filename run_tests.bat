@echo off
REM Script para ejecutar todos los tests de Django
cd /d %~dp0
call .venv\Scripts\activate
python manage.py test
pause
