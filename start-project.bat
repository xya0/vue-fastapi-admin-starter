@echo off & chcp 65001 >nul
setlocal

title 项目启动管理器
cd /d "%~dp0"

:MENU
cls
echo ========================================
echo           项目启动管理器
echo ========================================
echo.
echo   1. 一键启动项目（默认） 
echo   2. 仅启动前端 
echo   3. 仅启动后端 
echo   0. 退出 
echo ========================================
echo.
set "choice="
set /p "choice=请选择启动方式 [默认 1]："

if not defined choice set "choice=1"

if "%choice%"=="1" goto START_ALL
if "%choice%"=="2" goto START_FRONTEND
if "%choice%"=="3" goto START_BACKEND
if "%choice%"=="0" goto EXIT

echo.
echo [错误] 无效的选项，请重新选择。
pause
goto MENU

:START_ALL
echo.
echo [启动] 正在启动后端...

if not exist "%~dp0backend\start.bat" (
    echo [错误] 未找到 backend\start.bat
    pause
    goto MENU
)
start "项目后端" /D "%~dp0backend" "%ComSpec%" /k start.bat
echo [启动] 正在启动前端...
call :RUN_FRONTEND
goto MENU

:START_FRONTEND
echo.
call :RUN_FRONTEND
goto MENU

:START_BACKEND
echo.
if not exist "%~dp0backend\start.bat" (
    echo [错误] 未找到 backend\start.bat
    pause
    goto MENU
)
call "%~dp0backend\start.bat"
goto MENU

:RUN_FRONTEND
if not exist "%~dp0frontend\package.json" (
    echo [错误] 未找到 frontend\package.json
    pause
    exit /b 1
)
cd /d "%~dp0frontend"
echo [启动] 前端工作目录：%CD%
call pnpm run dev
cd /d "%~dp0"
exit /b

:EXIT
echo.
echo 已退出项目启动管理器。
endlocal
exit /b 0
```