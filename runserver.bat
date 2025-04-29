@echo off
cd /d C:\GenesisBackend
call venv\Scripts\activate
start http://127.0.0.1:8000/docs
python -m uvicorn app.main:app --reload
pause
