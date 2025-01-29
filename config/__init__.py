# config/__init__.py
from .generation import GenerationConfig
from .webui import WEBUI_CONFIG

# 生成配置
GENERATION_CONFIG = GenerationConfig()

# 模型配置
MODEL_CONFIG = {
    "model_path": "./models/deepseek-ai_DeepSeek-R1-Distill-Qwen-1.5B",  # 模型本地路径
    "reserved_memory": 1,        # 保留显存 (GB)
    "ai_warning": "内容由 AI 生成，请仔细甄别",  # 警告信息
    "input_max_length": 2000     # 输入最大长度
}

# WebUI输入配置
INPUT_CONFIG = {
    "min_length": 1,            # 输入最小长度
    "max_length": MODEL_CONFIG["input_max_length"]
}

# 导出配置
__all__ = [
    "GENERATION_CONFIG",
    "WEBUI_CONFIG",
    "MODEL_CONFIG",
    "INPUT_CONFIG"
]