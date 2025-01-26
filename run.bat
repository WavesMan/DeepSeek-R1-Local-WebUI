@echo off
REM 创建虚拟环境（如果不存在）
if not exist "deepseek_env" (
    echo 正在创建虚拟环境...
    python -m venv deepseek_env
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
call deepseek_env\Scripts\activate

REM 检查并下载模型（如果未下载）
echo 正在检查模型...
python downloadR1.py

REM 启动 Web 服务
echo 正在启动 Web 服务...
python webui.py

REM 等待模型加载完成
echo 等待模型加载完成...
timeout /t 10 >nul

REM 打开浏览器访问 Web UI
echo 模型加载完成，打开 Web UI...
start http://127.0.0.1:5000

REM 保持窗口打开以便查看输出
pause