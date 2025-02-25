# install_dependencies.py
import os
import sys
import questionary
import subprocess
from rich.console import Console

console = Console()

def install_deps(use_mirror=False, cuda_version=None):
    """安装依赖核心逻辑"""
    try:
        console.rule("[bold]正在安装依赖")
        
        # PyTorch安装
        torch_cmd = "pip install torch torchvision torchaudio"
        if cuda_version and cuda_version >= 12.1:
            torch_cmd += " --index-url https://download.pytorch.org/whl/cu121"
        else:
            torch_cmd += " --cpu"
        
        if use_mirror:
            torch_cmd += " -i https://mirrors.aliyun.com/pypi/simple/"
        
        console.print(f"[cyan]步骤 1/2: 安装PyTorch[/]\n{torch_cmd}")
        subprocess.run(torch_cmd, shell=True, check=True)
        
        # 其他依赖
        other_deps = ["transformers", "accelerate", "sentencepiece", "flask", ]
        dep_cmd = f"pip install {' '.join(other_deps)}"
        if use_mirror:
            dep_cmd += " -i https://mirrors.aliyun.com/pypi/simple/"
        
        console.print(f"\n[cyan]步骤 2/2: 安装其他依赖[/]\n{dep_cmd}")
        subprocess.run(dep_cmd, shell=True, check=True)
        
        console.print("[bold green]✅ 所有依赖安装完成![/]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ 安装失败: {e.stderr}[/]")
        return False

def check_cuda():
    """检测CUDA版本"""
    try:
        result = subprocess.run(
            "nvcc --version",
            shell=True,
            capture_output=True,
            text=True
        )
        if "release" in result.stdout:
            version_str = result.stdout.split("release")[1].split(",")[0].strip()
            return float(version_str)
        return None
    except Exception:
        return None

def interactive_install():
    """交互式安装入口"""
    console.print("[bold]🔧 依赖安装向导[/]")
    
    # 镜像源选择
    use_mirror = questionary.select(
        "选择PyPI镜像源:",
        choices=[
            questionary.Choice("阿里云镜像（推荐）", True),
            questionary.Choice("官方源", False),
        ],
        default=True
    ).ask()
    
    # CUDA检测
    cuda_ver = check_cuda()
    if cuda_ver:
        console.print(f"[green]✔ 检测到CUDA {cuda_ver}[/]")
        install_cuda = cuda_ver >= 12.1
    else:
        console.print("[yellow]⚠ 未检测到CUDA[/]")
        install_cuda = questionary.confirm("是否安装CPU版本？", default=True).ask()
    
    return install_deps(use_mirror, cuda_ver)

if __name__ == "__main__":
    interactive_install()