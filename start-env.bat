@echo off
:: 切换到当前脚本所在目录（即项目根目录），确保相对路径正确
cd /d "%~dp0"

:: 激活 backend 文件夹下的 .venv 虚拟环境
call backend\.venv\Scripts\activate.bat

:: 验证是否激活成功（可选）
REM where python
REM echo Virtual environment activated.

:: 关键命令：保持窗口开启并进入交互模式
cmd /k


