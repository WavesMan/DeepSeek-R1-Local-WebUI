# core/model_manager.py
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from config import MODEL_CONFIG

class ModelManager:
    def __init__(self, model_path):
        self.model_path = model_path
        self.device = self._get_device()
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _get_device(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        if device == "cuda":
            self._configure_gpu_memory()
        
        return device

    def _configure_gpu_memory(self):
        total_memory = torch.cuda.get_device_properties(0).total_memory
        print(f"GPU Total Memory: {total_memory / 1024 ** 3:.2f} GB")
        
        reserved_memory = MODEL_CONFIG.reserved_memory * 1024**3
        max_memory = total_memory - reserved_memory
        memory_fraction = max_memory / total_memory
        torch.cuda.set_per_process_memory_fraction(memory_fraction, device=0)
        print(f"Set max memory limit: {max_memory / 1024 ** 3:.2f} GB")

    def _load_model(self):
        print(f"从路径加载模型中： {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self.model = self.model.to(self.device)
        print("模型加载成功")

    def create_streamer(self):
        return TextStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )

    def get_generation_inputs(self, input_text):
        return self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)