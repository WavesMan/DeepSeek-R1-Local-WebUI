# core/model_manager.py
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

class ModelManager:
    def __init__(self, model_path):
        self.model_path = model_path
        self.device_info = self._detect_hardware()
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _detect_hardware(self):
        """检测硬件环境并返回最佳设备配置"""
        device_info = {
            "device_type": "cpu",
            "device_id": -1,
            "torch_dtype": torch.float32
        }

        if torch.cuda.is_available():
            # 分析所有可用GPU
            gpu_list = []
            for i in range(torch.cuda.device_count()):
                prop = torch.cuda.get_device_properties(i)
                free_mem = prop.total_memory - torch.cuda.memory_allocated(i)
                gpu_list.append({
                    "index": i,
                    "name": prop.name,
                    "total_mem": prop.total_memory,
                    "free_mem": free_mem
                })

            # 选择可用显存最大的GPU
            if gpu_list:
                best_gpu = max(gpu_list, key=lambda x: x["free_mem"])
                if best_gpu["free_mem"] > 3 * 1024**3:  # 至少3GB可用显存
                    device_info.update({
                        "device_type": "cuda",
                        "device_id": best_gpu["index"],
                        "torch_dtype": torch.float16
                    })
                    print(f"选择GPU {best_gpu['index']} ({best_gpu['name']})")
                    print(f"可用显存: {best_gpu['free_mem']/1024**3:.1f}GB")

        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device_info["device_type"] = "mps"

        return device_info

    def _load_model(self):
        """加载模型到指定设备"""
        print(f"加载模型: {os.path.basename(self.model_path)}")

        # 加载tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        # 配置设备映射
        device_map = "auto" if self.device_info["device_type"] == "cuda" else None

        # 加载模型
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map=device_map,
            torch_dtype=self.device_info["torch_dtype"],
            low_cpu_mem_usage=True,
            local_files_only=True
        )

        # 如果自动分配失败，手动指定设备
        if not device_map:
            self.model = self.model.to(self.device_info["device_type"])

        print(f"模型加载完成 | 设备: {self.model.device} | 精度: {self.device_info['torch_dtype']}")

    def create_streamer(self):
        """创建流式输出处理器"""
        return TextStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )