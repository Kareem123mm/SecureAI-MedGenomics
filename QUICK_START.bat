@echo off
REM Quick Start - SecureAI-MedGenomics Backend Only
echo.
echo Starting SecureAI-MedGenomics Backend...
echo.

set PYTHON="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"

cd /d "%~dp0backend"

echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

%PYTHON% integrated_main.py

pause
