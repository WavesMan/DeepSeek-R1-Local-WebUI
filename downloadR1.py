from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# 模型名称（替换为实际的Hugging Face模型路径）
model_name = "deepseek/DeepSeek-R1-1.5B"
local_model_path = "./deepseek_r1_1.5b"

# 检查模型是否已下载
if os.path.exists(local_model_path):
    print(f"模型已存在于 {local_model_path}，跳过下载。")
else:
    print(f"模型未找到，开始下载...")

    # 下载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")

    # 保存到本地
    model.save_pretrained(local_model_path)
    tokenizer.save_pretrained(local_model_path)

    print(f"模型和分词器已下载并保存到 {local_model_path}。")