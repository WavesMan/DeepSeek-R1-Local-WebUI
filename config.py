# config.py

# 模型路径配置
MODEL_PATH = "./deepseek_r1_1.5b"  # 模型本地路径

# 生成文本的配置
GENERATION_CONFIG = {
    "max_length": 500,  # 生成文本的最大长度
    "num_beams": 1,  # beam search 的 beam 数量
    "temperature": 0.7,  # 温度参数，控制生成文本的随机性
    "top_k": 50,  # top-k 采样参数
    "top_p": 0.9,  # top-p 采样参数
    "do_sample": True,  # 是否使用采样
}

# WebUI 配置
WEBUI_CONFIG = {
    "host": "127.0.0.1",  # WebUI 的主机地址
    "port": 5000,  # WebUI 的端口号
    "stream_delay": 0.1,  # 流式输出的延迟时间（秒）
}



# 其他配置
AI_WARNING_MESSAGE = "内容由 AI 生成，请仔细甄别"  # AI 生成内容的提示信息