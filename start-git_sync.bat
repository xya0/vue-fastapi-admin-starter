@echo off
:: 设置编码为 UTF-8，防止中文乱码
chcp 65001 >nul

:: 配置你的主分支名称（通常为 main 或 master）
set BRANCH=main

echo ==========================================
echo   Git 状态检查与同步工具
echo ==========================================
echo.

echo [1/2] 正在切换到 %BRANCH% 分支...
git checkout %BRANCH%
if errorlevel 1 goto error

echo [2/2] 正在从 GitHub 获取最新状态 (git fetch)...
git fetch origin %BRANCH%
if errorlevel 1 goto error

echo.
echo ==========================================
echo   检查结果：
echo ==========================================

:: 检查本地是否有未提交的修改
git diff --quiet
set HAS_UNCOMMITTED=%errorlevel%

:: 检查本地分支与远程分支的落后/领先状态
for /f "tokens=2" %%i in ('git rev-parse HEAD') do set LOCAL_COMMIT=%%i
for /f "tokens=2" %%i in ('git rev-parse origin/%BRANCH%') do set REMOTE_COMMIT=%%i

git rev-parse @{u} >nul 2>&1
if errorlevel 1 (
    echo [提示] 当前分支未关联远程分支。
    goto menu
)

git diff --quiet origin/%BRANCH% %BRANCH%
set HAS_DIFF=%errorlevel%

:: 判断状态
if "%LOCAL_COMMIT%"=="%REMOTE_COMMIT%" (
    if %HAS_UNCOMMITTED% EQU 0 (
        echo 【状态】本地代码与 GitHub **完全一致**，且工作区干净。
    ) else (
        echo 【状态】本地有**未提交的修改**，但提交历史与 GitHub 一致。
    )
) else (
    echo 【状态】本地与 GitHub **存在差异**（可能领先或落后）。
)

echo.
echo ------------------------------------------
:menu
echo 请选择要执行的操作： 
echo   [1] 本地覆盖远程 (强推本地代码)  （用本地新代码替换远程旧代码） 
echo   [2] 远程覆盖本地 (重置本地代码)  （会丢弃本地所有未提交修改） 
echo   [3] 合并推送代码 (保留双方修改)  （自动 stash, pull, pop 并 push） 
echo   [4] 退出脚本 
echo.

set /p choice=请输入选项编号 (1-4): 

if "%choice%"=="1" goto option1
if "%choice%"=="2" goto option2
if "%choice%"=="3" goto option3
if "%choice%"=="4" goto end

echo 无效的选项，请重新选择。
goto menu

:: ------------------------------------------
:: 选项 1：以本地代码为准，强推覆盖远程
:: ------------------------------------------
:option1
echo.
echo [警告] 即将用本地代码强行覆盖远程 GitHub！远程的旧代码将会丢失！
set /p confirm=确定继续吗？(Y/N): 
if /i "%confirm%" NEQ "Y" (
    echo 操作已取消。
    goto end
)

:: 确保本地变动已提交
git status
echo 正在将本地所有修改提交并推送到远端...
git add .
set /p commit_msg=请输入本次提交的备注信息 (默认: force update): 
if "%commit_msg%"=="" set commit_msg=force update
git commit -m "%commit_msg%"

echo 正在强行推送到 GitHub (git push --force)...
git push origin %BRANCH% --force
if errorlevel 1 goto error

echo.
echo [成功] 已成功以本地代码为准覆盖了远程 GitHub！
goto end

:: ------------------------------------------
:: 选项 2：强制本地同步为远程最新
:: ------------------------------------------
:option2
echo.
echo [警告] 即将强制丢弃本地所有修改并与 GitHub 对齐！
set /p confirm=确定继续吗？(Y/N): 
if /i "%confirm%" NEQ "Y" (
    echo 操作已取消。
    goto end
)

echo 正在强制重置 (git reset --hard)...
git reset --hard origin/%BRANCH%
echo 正在清理未追踪文件 (git clean)...
git clean -fd
echo.
echo [成功] 本地代码已强制同步为 GitHub 最新状态！
goto end

:: ------------------------------------------
:: 选项 3：合并本地修改并推送
:: ------------------------------------------
:option3
echo.
echo 正在暂存本地修改 (git stash)...
git stash

echo 正在拉取远程最新代码 (git pull)...
git pull origin %BRANCH%
if errorlevel 1 (
    echo.
    echo [冲突提醒] 自动拉取合并时遇到冲突，请手动解决冲突后再次提交！
    git stash pop
    goto error
)

echo 正在恢复本地暂存的修改 (git stash pop)...
git stash pop
if errorlevel 1 (
    echo.
    echo [提示] 恢复暂存时可能存在小冲突，请在编辑器中手动解决。
    goto end
)

echo 正在添加并提交本地修改...
git add .
set /p commit_msg=请输入本次提交的备注信息 (默认: update): 
if "%commit_msg%"=="" set commit_msg=update
git commit -m "%commit_msg%"

echo 正在推送到 GitHub (git push)...
git push origin %BRANCH%
if errorlevel 1 goto error

echo.
echo [成功] 本地修改已成功合并并推送到 GitHub！
goto end

:: ------------------------------------------
:: 错误与结束处理
:: ------------------------------------------
:error
echo.
echo [错误] 操作过程中断，请检查网络或 Git 状态。

:end
echo.
pause