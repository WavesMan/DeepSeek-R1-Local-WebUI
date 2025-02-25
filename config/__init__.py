# config/__init__.py
import os
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class ConfigMeta(type):
    """配置元类实现自动类型转换和保存功能"""
    def __getattr__(cls, name):
        env_var = f"{cls.prefix}_{name}"
        value = os.getenv(env_var, cls.defaults.get(name))
        
        # 自动类型转换
        if isinstance(value, str):
            if value.lower() in ('true', 'false'):
                return value.lower() == 'true'
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    if len(value) > 1 and value[0] == value[-1] and value[0] in ('"', "'"):
                        return value[1:-1]
        return value

    def __setattr__(cls, name, value):
        env_var = f"{cls.prefix}_{name}"
        os.environ[env_var] = str(value)
        
    def save(cls):
        """将当前配置持久化到.env文件"""
        env_path = BASE_DIR / '.env'
        existing_lines = []
        
        # 读取现有配置
        if env_path.exists():
            with open(env_path, 'r') as f:
                existing_lines = [line.strip() for line in f if line.strip()]
        
        # 过滤并保留其他配置项
        new_lines = []
        for line in existing_lines:
            if not line.startswith(f"{cls.prefix}_"):
                new_lines.append(line)
        
        # 添加当前配置项
        for name in cls.defaults.keys():
            value = getattr(cls, name)
            new_lines.append(f"{cls.prefix}_{name.upper()}={value}")
        
        # 写入文件
        with open(env_path, 'w') as f:
            f.write("\n".join(new_lines) + "\n")

# === 模型配置 ===
class ModelConfig(metaclass=ConfigMeta):
    prefix = "MODEL"
    defaults = {
        "reserved_memory": 1,
        "input_max_length": 2000,
        "ai_warning": "本内容由 AI 生成，请仔细甄别"
    }
    save = classmethod(ConfigMeta.save)

# === WebUI 配置 ===
class WebUIConfig(metaclass=ConfigMeta):
    prefix = "WEBUI"
    defaults = {
        "host": "127.0.0.1",
        "port": 5000,
        "debug": False
    }
    save = classmethod(ConfigMeta.save)

# === 生成参数配置 ===
class GenerationConfig(metaclass=ConfigMeta):
    prefix = "GEN"
    defaults = {
        "max_length": 500,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "do_sample": True
    }
    save = classmethod(ConfigMeta.save)

# 导出配置对象
MODEL_CONFIG = ModelConfig()
WEBUI_CONFIG = WebUIConfig()
GENERATION_CONFIG = GenerationConfig()