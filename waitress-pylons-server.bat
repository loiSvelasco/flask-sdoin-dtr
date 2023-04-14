@ECHO off
color 0b
title Server running ~sdoin.dtr @ ipv4:5000 ~ by Louis Velasco 
type brand.txt
ECHO.
ECHO Serving ~sdoin.dtr on : http://192.168.102.25:5001
ECHO Do not close this window.
call venv-dtr\Scripts\activate
python server.py
pause

