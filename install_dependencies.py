import subprocess 
import sys 
import platform 
 
def run_command(command):
    """运行命令并捕获输出"""
    try:
        result = subprocess.run( 
            command,
            check=True,
            shell=True,
            capture_output=True,
            text=True 
        )
        print("成功执行命令:")
        print(result.stdout.strip()) 
        return True 
    except subprocess.CalledProcessError as e:
        print(f"错误：{e}")
        print(f"命令输出:\n{e.output}") 
        return False 
 
def get_cuda_version():
    """检测系统中安装的 CUDA 版本"""
    try:
        result = subprocess.run( 
            "nvcc --version",
            shell=True,
            capture_output=True,
            text=True 
        )
        output = result.stdout.strip() 
        if "release" in output:
            version_line = output.split("release")[1].split(",")[0].strip() 
            version = version_line.split()[0] 
            return version 
        return None 
    except subprocess.CalledProcessError:
        return None 
 
def main():
    print("开始安装依赖项...")
    
    # 检测 CUDA 版本 
    cuda_version = get_cuda_version()
    if cuda_version:
        print(f"检测到 CUDA 版本: {cuda_version}")
    else:
        print("未检测到 CUDA 或 nvcc 未安装。")

    # 询问用户是否使用阿里云镜像源 
    while True:
        user_input = input("\n是否使用阿里云镜像源加速安装？(y/n): ").strip().lower()
        if user_input == 'y':
            mirror_url = "--mirror-url https://mirrors.aliyun.com/pypi/simple/" 
            print("\n将使用阿里云镜像源进行安装...")
            break 
        elif user_input == 'n':
            mirror_url = ""
            print("\n将使用默认源进行安装...")
            break 
        else:
            print("无效输入，请输入 'y' 或 'n'。")
    
    # 询问用户是否已安装 CUDA 12.1+
    while True:
        user_input = input("\n是否已经安装 CUDA 12.1 或更高版本？(y/n): ").strip().lower()
        if user_input == 'y':
            # 安装带 CUDA 支持的 PyTorch 
            pytorch_command = (
                "pip3 install torch torchvision torchaudio "
                "--index-url https://download.pytorch.org/whl/cu121" 
            )
            if not run_command(pytorch_command):
                print("PyTorch 安装失败，退出安装...")
                return 
            break 
        elif user_input == 'n':
            # 安装 CPU 版本的 PyTorch 
            print("\n将安装 CPU 版本的 PyTorch...")
            pytorch_command = "pip3 install torch torchvision torchaudio --cpu"
            if not run_command(pytorch_command):
                print("PyTorch 安装失败，退出安装...")
                return 
            break 
        else:
            print("无效输入，请输入 'y' 或 'n'。")
    
    # 安装其他依赖 
    other_packages = "pip3 install transformers accelerate sentencepiece flask"
    if not run_command(other_packages):
        print("其他依赖安装失败，退出安装...")
        return 
    
    print("所有依赖安装完成！")
 
if __name__ == "__main__":
    main()