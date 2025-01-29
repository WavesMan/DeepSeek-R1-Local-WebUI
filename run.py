from flask import Flask 
from config import WEBUI_CONFIG 
from web.routes  import create_routes 
import torch 
import os 
 
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
    
    # 让用户选择模型 
    selected_model = select_model()
    
    # 加载选定的模型 
    from core.model_manager  import ModelManager 
    model_manager = ModelManager(os.path.join("models",  selected_model))
    
    app = Flask(__name__)
    app.register_blueprint(create_routes(model_manager)) 
    
    print("\n[服务启动参数]")
    print(f"  Host: {WEBUI_CONFIG['host']}")
    print(f"  Port: {WEBUI_CONFIG['port']}")
    print(f"  Debug模式: {'开启' if WEBUI_CONFIG['debug'] else '关闭'}\n")
    
    app.run(**WEBUI_CONFIG) 