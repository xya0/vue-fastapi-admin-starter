@echo off
:: 设置字符集为 UTF-8，防止中文或特殊字符乱码
chcp 65001 >nul

:: 切换到当前脚本所在的根目录
cd /d "%~dp0"
echo [INFO] 当前工作目录: %CD%


:: 定义项目根目录和虚拟环境路径
set "BACKEND_DIR=%~dp0backend" & REM 将当前批处理脚本所在的目录下的backend 
set "VENV_PATH=%BACKEND_DIR%\.venv" & REM 虚拟环境文件夹名称 
set "MAIN_SCRIPT=%BACKEND_DIR%\app\main.py" & REM 主程序名称 


:: 检查 UV 是否可用
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] UV is not installed or not in PATH.
    echo Please install UV first: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)


:: 检查本地是否存在虚拟环境文件夹
if not exist "%VENV_PATH%\" (
    echo [INFO] 未检测到虚拟环境，正在使用 uv 创建环境...
	cd /d "%BACKEND_DIR%"
    uv venv --python 3.11
    if errorlevel 1 (
        echo [ERROR] 虚拟环境创建失败，请确保已安装 uv 工具。
        pause
        exit /b 1
    )
) else (
    echo [INFO] 检测到本地已存在虚拟环境。
	cd /d "%BACKEND_DIR%"
)

:: 激活虚拟环境 
echo [INFO] 正在激活虚拟环境...
call "%VENV_PATH%\Scripts\activate.bat"


:: 检查并执行指定的 Python 脚本
if exist "%MAIN_SCRIPT%" (
    echo [INFO] 开始执行脚本: %MAIN_SCRIPT%
    echo ------------------------------------------
    REM python "%MAIN_SCRIPT%"
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo ------------------------------------------
    echo [INFO] 脚本执行完毕。
) else (
    echo [ERROR] 未找到指定的 Python 脚本: %MAIN_SCRIPT%
)

:: 保持窗口打开以查看输出结果
pause