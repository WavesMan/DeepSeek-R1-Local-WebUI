# scripts/model_downloader.py
import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_CHOICES = {
    "1": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "2": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "3": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "4": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "5": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "6": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
}

def show_model_menu() -> None:
    """显示模型选择菜单"""
    print("\n可选模型列表：")
    for num, model in MODEL_CHOICES.items():
        print(f"  [{num}] {model.split('/')[-1]}")
    print("  [q] 退出")

def get_user_choice() -> str:
    """获取用户选择的模型"""
    while True:
        choice = input("\n请输入要下载的模型编号 (1-6/q): ").strip().lower()
        if choice == 'q':
            sys.exit("用户取消下载")
        if choice in MODEL_CHOICES:
            return MODEL_CHOICES[choice]
        print("错误：无效的选项，请输入1-6或q退出")

def download_model(model_id: str) -> str:
    """下载指定模型到本地"""
    local_dir = os.path.join("models", model_id.replace("/", "_"))
    
    if os.path.exists(local_dir):
        print(f"\n模型已存在于: {local_dir}")
        return local_dir

    print(f"\n开始下载模型: {model_id}")
    try:
        print("下载分词器...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("下载模型主体...")
        model = AutoModelForCausalLM.from_pretrained(model_id)

        os.makedirs(local_dir, exist_ok=True)
        print("保存到本地...")
        model.save_pretrained(local_dir)
        tokenizer.save_pretrained(local_dir)
        
        print(f"\n✅ 模型已保存至: {local_dir}")
        return local_dir
    except Exception as e:
        print(f"\n❌ 下载失败: {str(e)}")
        if os.path.exists(local_dir):
            os.rmdir(local_dir)
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + "="*40)
    print("DeepSeek-R1 模型下载工具")
    print("="*40)
    
    show_model_menu()
    selected_model = get_user_choice()
    model_path = download_model(selected_model)
    
    print("\n提示：请将以下路径复制到config.py的MODEL_CONFIG中：")
    print(f"model_path = '{model_path}'")