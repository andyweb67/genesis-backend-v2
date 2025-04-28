@echo off
set PYTHONPATH=.
python -m uvicorn app.main:app --reload
pause
