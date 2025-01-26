from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# 定义可下载的模型列表
models = {
    "1": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "2": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "3": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "4": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "5": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "6": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
}

# 显示模型选项
print("请选择要运行/下载的模型：")
for key, value in models.items():
    print(f"{key}: {value}")

# 获取用户输入
choice = input("输入选项编号: ")

# 检查用户输入是否有效
if choice in models:
    model_name = models[choice]
    local_model_path = f"./models/{model_name.replace('/', '_')}"
    
    # 检查模型是否已下载
    if os.path.exists(local_model_path):
        print(f"模型已存在于 {local_model_path}，跳过下载。")
    else:
        print(f"模型未找到，开始下载 {model_name}...")

        # 下载模型和分词器
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # 保存到本地
        model.save_pretrained(local_model_path)
        tokenizer.save_pretrained(local_model_path)

        print(f"模型和分词器已下载并保存到 {local_model_path}。")
    
    # 清除 model_path.txt 文件内容（如果存在）
    if os.path.exists("model_path.txt"):
        with open("model_path.txt", "w") as f:
            f.write("")  # 清空文件内容
    
    # 将模型路径保存到临时文件
    with open("model_path.txt", "w") as f:
        f.write(local_model_path)
else:
    print("无效的选项编号。")