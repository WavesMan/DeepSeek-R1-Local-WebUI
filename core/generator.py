# core/generator.py
import torch
from transformers import GenerationConfig

class TextGenerator:
    def __init__(self, model_manager, generation_config):
        self.model_manager = model_manager
        self.generation_config = generation_config

    def generate_stream(self, input_text):
        inputs = self.model_manager.get_generation_inputs(input_text)
        streamer = self.model_manager.create_streamer()

        generation_args = {
            **inputs,
            **self.generation_config.to_dict(),
            "pad_token_id": self.model_manager.tokenizer.eos_token_id,
            "streamer": streamer,
        }

        with torch.no_grad():
            yield from self.model_manager.model.generate(**generation_args)