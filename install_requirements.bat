@echo off  

REM 创建虚拟环境（如果不存在）
if not exist "deepseek_env" (
    echo 正在创建虚拟环境...
    python -m venv deepseek_env
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call deepseek_env\Scripts\activate

REM 询问用户是否使用国内镜像源
set /p use_mirror="是否使用国内镜像源（阿里云）？(y/n): "

REM 设置镜像源（如果用户选择使用）
if "%use_mirror%"=="y" (
    echo 正在设置阿里云镜像源...
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
) else (
    echo 不使用镜像源，从官方源下载。
)

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

echo 安装完成！
echo 按任意键退出...
pause>>nul