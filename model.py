# model.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from config import MODEL_PATH, GENERATION_CONFIG

class DeepSeekModel:
    def __init__(self, model_path=MODEL_PATH):
        # 动态设置设备
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")

        if self.device == "cuda":
            # 获取当前 GPU 的总显存
            total_memory = torch.cuda.get_device_properties(0).total_memory
            print(f"GPU 总显存: {total_memory / 1024 ** 3:.2f} GB")

            # 设置显存使用上限（保留 1GB 显存）
            reserved_memory = 1 * 1024 ** 3  # 1GB
            max_memory = total_memory - reserved_memory
            memory_fraction = max_memory / total_memory
            torch.cuda.set_per_process_memory_fraction(memory_fraction, device=0)
            print(f"设置显存使用上限: {max_memory / 1024 ** 3:.2f} GB")

        # 加载模型和分词器
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

        # 将模型移动到对应设备
        self.model = self.model.to(self.device)

    def generate_text(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                pad_token_id=self.tokenizer.eos_token_id,
                **GENERATION_CONFIG,
                streamer=streamer,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text