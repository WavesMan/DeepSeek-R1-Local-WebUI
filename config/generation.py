# config/generation.py
from transformers import GenerationConfig

class GenerationConfig(GenerationConfig):
    def __init__(self):
        super().__init__(
            max_length=500,
            num_beams=1,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            do_sample=True,
            pad_token_id=None  # Will be set dynamically
        )