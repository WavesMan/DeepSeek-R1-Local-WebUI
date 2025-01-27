# config/__init__.py
import os
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).parent.parent
MODEL_BASE_DIR = BASE_DIR / "models"

# Web服务配置
WEBUI_CONFIG = {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": False
}

# 流式响应配置
STREAM_CONFIG = {
    "stream_delay": 0.1
}

# 生成参数配置
GENERATION_CONFIG = {
    "max_length": 500,
    "temperature": 0.7,
    "top_p": 0.9,
    "do_sample": True
}

# 模型配置
MODEL_CONFIG = {
    "model_path": str(MODEL_BASE_DIR / "deepseek-ai_DeepSeek-R1-Distill-Qwen-1.5B"),
    "reserved_memory": 1,  # 保留显存(GB)
    "ai_warning": "内容由 AI 生成，请仔细甄别"
}