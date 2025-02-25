# scripts/model_downloader.py
import os
import sys
import questionary
from rich.console import Console
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

console = Console()

MODEL_MAP = {
    "deepseek-ai/1.5B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "deepseek-ai/7B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "deepseek-ai/8B": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "deepseek-ai/14B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "deepseek-ai/32B": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "deepseek-ai/70B": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
}

def download_model(model_size: str):
    """下载指定模型"""
    model_id = MODEL_MAP.get(model_size)
    if not model_id:
        console.print(f"[bold red]错误: 不支持的模型规格 {model_size}[/]")
        return False

    local_dir = Path("models") / model_id.replace("/", "_")
    
    if local_dir.exists():
        console.print(f"[yellow]⚠ 模型已存在: {local_dir}[/]")
        return True

    try:
        console.rule(f"[bold]正在下载 {model_size} 模型")
        
        console.print("[cyan]步骤 1/2: 下载分词器[/]")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        console.print("[cyan]步骤 2/2: 下载模型主体[/]")
        model = AutoModelForCausalLM.from_pretrained(model_id)

        local_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(local_dir)
        tokenizer.save_pretrained(local_dir)
        
        console.print(f"[bold green]✅ 模型已保存至: {local_dir}[/]")
        return True
    except Exception as e:
        console.print(f"[bold red]❌ 下载失败: {str(e)}[/]")
        return False

def interactive_download():
    """交互式下载入口"""
    choice = questionary.select(
        "\n".join([
            f"选择要下载的模型规格:",
            f"\n按 Ctrl+C 返回上一级"
        ]),
        choices=[
            questionary.Choice(
                f"{size} ({MODEL_MAP[size].split('/')[-1]})",
                value=size
            ) for size in MODEL_MAP
        ],
        qmark="📥",
        # pointer="👉"
    ).ask()
    
    if choice:
        success = download_model(choice)
        if success:
            console.print(f"\n[bold]下一步: 运行 [cyan]python cli.py run[/] 启动服务[/]")

if __name__ == "__main__":
    interactive_download()