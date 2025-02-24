# run.py
from flask import Flask
from core.model_manager import ModelManager
import os
import torch
import platform

def print_hardware_report():
    """打印硬件报告"""
    print("\n[硬件检测报告]")
    print(f"PyTorch版本: {torch.__version__}")
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

def select_model():
    """让用户选择要使用的模型"""
    model_dir = "models"
    model_list = os.listdir(model_dir) 
    
    print("\n[模型选择]")
    print("请选择要使用的模型：")
    for idx, model in enumerate(model_list, start=1):
        print(f"{idx}. {model}")
    
    while True:
        try:
            choice = int(input("\n请输入模型编号（例如：1）：")) - 1 
            if 0 <= choice < len(model_list):
                selected_model = model_list[choice]
                print(f"\n已选择模型：{selected_model}\n")
                return selected_model 
            else:
                print("输入的编号不在范围内，请重新输入。")
        except ValueError:
            print("请输入有效的数字编号。")
 
def print_hardware_report():
    """打印详细的硬件信息报告"""
    print("\n[硬件检测报告]")
    print(f"PyTorch版本: {torch.__version__}")
    
    # CUDA信息 
    if torch.cuda.is_available(): 
        print(f"CUDA版本: {torch.version.cuda}") 
        print(f"检测到 {torch.cuda.device_count()}  个GPU:")
        for i in range(torch.cuda.device_count()): 
            prop = torch.cuda.get_device_properties(i) 
            print(f"  GPU {i}: {prop.name}") 
            print(f"    显存总量: {prop.total_memory/1024**3:.1f}GB") 
            print(f"    当前占用: {torch.cuda.memory_allocated(i)/1024**3:.1f}GB") 
    else:
        print("未检测到CUDA设备")
 
if __name__ == "__main__":
    print_hardware_report()
    selected_model = select_model()
    
    from core.model_manager import ModelManager
    model_manager = ModelManager(os.path.join("models", selected_model))
    
    # 关键修改：正确初始化Flask应用
    app = Flask(__name__,
        static_url_path='/static',
        static_folder='static',
        template_folder='templates'
    )
    
    from web.routes import create_routes
    app.register_blueprint(create_routes(model_manager))
    
    # 打印调试信息
    print("\n=== 当前Web配置 ===")
    from config import WEBUI_CONFIG
    print(f"  Host: {WEBUI_CONFIG['host']}")
    print(f"  Port: {WEBUI_CONFIG['port']}")
    print(f"  Debug模式: {'开启' if WEBUI_CONFIG['debug'] else '关闭'}")
    
    print("\n=== 已注册路由 ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
    
    app.run(**WEBUI_CONFIG)