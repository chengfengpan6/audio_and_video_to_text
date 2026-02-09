@echo off
title Whisper 本地语音识别启动器
color 0A

echo ========================================================
echo        正在启动 Whisper AI (Large-v3)...
echo        请勿关闭此窗口，网页会在浏览器中自动打开
echo ========================================================

:: 1. 确保进入 D 盘
d:

:: 2. 确保进入项目文件夹 (防止路径错误)
cd "D:\whisper_project"

:: 3. 直接使用虚拟环境的 Python 运行代码
:: 这样写比 activate 更稳定
".\venv\Scripts\python.exe" web_ui.py

:: 4. 如果程序崩溃，暂停显示报错信息，而不是直接闪退
pause