@echo off
python app.py
curl http://localhost:5000/refresh
pause