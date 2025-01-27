# run.py
from flask import Flask
from config import WEBUI_CONFIG
from web.routes import bp
import torch

def print_hardware_report():
    """打印详细的硬件信息报告"""
    print("\n[硬件检测报告]")
    print(f"PyTorch版本: {torch.__version__}")
    
    # CUDA信息
    if torch.cuda.is_available():
        print(f"CUDA版本: {torch.version.cuda}")
        print(f"检测到 {torch.cuda.device_count()} 个GPU:")
        for i in range(torch.cuda.device_count()):
            prop = torch.cuda.get_device_properties(i)
            print(f"  GPU {i}: {prop.name}")
            print(f"    显存总量: {prop.total_memory/1024**3:.1f}GB")
            print(f"    当前占用: {torch.cuda.memory_allocated(i)/1024**3:.1f}GB")
    else:
        print("未检测到CUDA设备")

if __name__ == "__main__":
    print_hardware_report()
    
    app = Flask(__name__)
    app.register_blueprint(bp)
    
    print("\n[服务启动参数]")
    print(f"  Host: {WEBUI_CONFIG['host']}")
    print(f"  Port: {WEBUI_CONFIG['port']}")
    print(f"  Debug模式: {'开启' if WEBUI_CONFIG['debug'] else '关闭'}\n")
    
    app.run(**WEBUI_CONFIG)