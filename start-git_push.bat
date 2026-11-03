@echo off
:: 设置编码为 UTF-8，防止中文提示词乱码
chcp 65001 >nul

echo =============================================
echo               Git 自动提交与推送             
echo =============================================

:: 1. 检查是否存在 .git 文件夹
if not exist ".git" (
    echo [错误] 当前目录不是一个 Git 仓库，请先运行 git init
    goto end
)

:: 2. 自动获取当前所在的分支名称
for /f "tokens=*" %%i in ('git branch --show-current') do set BRANCH=%%i

if "%BRANCH%"=="" (
    echo [错误] 无法获取当前分支，请确保本地至少有一次提交。
    goto end
)

echo [当前分支] %BRANCH%

:: 3. 添加所有修改到暂存区 
echo [1/3] 正在添加文件到暂存区... 

git add .

:: 4. 提示输入提交信息（如果没有输入，则使用默认信息）
set /p msg="[2/3] 请输入 Commit 提交信息 (直接回车则使用默认信息): "
if "%msg%"=="" (
    set "msg=Auto-commit: %date% %time%"
)

:: 执行提交
git commit -m "%msg%"

:: 5. 推送到 GitHub
echo [3/3] 正在推送到 GitHub (%BRANCH% 分支)...
git push origin %BRANCH%

if %errorlevel% equ 0 (
    echo =============================================
    echo [成功] 代码已成功推送到 GitHub！
    echo =============================================
) else (
    echo =============================================
    echo [失败] 推送过程中出现错误，请检查网络或权限。
    echo =============================================
)

:end
pause
