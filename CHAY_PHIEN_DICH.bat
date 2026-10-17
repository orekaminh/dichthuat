@echo off
cd /d "%~dp0"
title Phien dich truc tiep - KHONG DONG CUA SO NAY khi dang hop
echo.
echo  Phien dich truc tiep dang chay tai: http://localhost:8765
echo  Giu cua so nay mo trong luc hop. Dong cua so = tat chuong trinh.
echo.
start "" chrome "http://localhost:8765/index.html"
python serve.py
