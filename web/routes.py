# web/routes.py
import json
import time
import torch
import os
from transformers import TextIteratorStreamer
from threading import Thread
from flask import (
    Blueprint, 
    request, 
    Response, 
    jsonify, 
    render_template,
    stream_with_context
)

class GenerationConfig:
    @property
    def max_length(self):
        return int(os.getenv('GEN_MAX_LENGTH', 500))
    
    @property
    def temperature(self):
        return float(os.getenv('GEN_TEMPERATURE', 0.7))
    
    @property
    def top_k(self):
        return int(os.getenv('GEN_TOP_K', 50))
    
    @property
    def top_p(self):
        return float(os.getenv('GEN_TOP_P', 0.9))
    
    @property
    def do_sample(self):
        return os.getenv('GEN_DO_SAMPLE', 'True').lower() == 'true'

def create_routes(model_manager):
    bp = Blueprint('main', __name__)
    gen_config = GenerationConfig()

    @bp.route('/')
    def index():
        return render_template(
            'index.html',
            ai_warning=os.getenv('AI_WARNING', '内容由AI生成，请仔细甄别')
        )

    @bp.route('/api/chat', methods=['POST'])
    def chat_api():
        if not request.is_json:
            return jsonify({"error": "需要JSON格式请求"}), 415

        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({"error": "输入内容不能为空"}), 400

        def generate():
            try:
                start_time = time.time()
                full_response = ""
                
                streamer = TextIteratorStreamer(
                    model_manager.tokenizer,
                    skip_prompt=True,
                    timeout=60
                )

                inputs = model_manager.tokenizer(
                    user_input,
                    return_tensors="pt",
                    max_length=int(os.getenv('MODEL_INPUT_MAX_LENGTH', 2000)),
                    truncation=True,
                    padding=True
                ).to(model_manager.model.device)

                generation_config = {
                    **inputs,
                    "max_new_tokens": gen_config.max_length,
                    "temperature": gen_config.temperature,
                    "top_k": gen_config.top_k,
                    "top_p": gen_config.top_p,
                    "do_sample": gen_config.do_sample,
                    "pad_token_id": model_manager.tokenizer.eos_token_id,
                    "streamer": streamer
                }

                thread = Thread(target=model_manager.model.generate, kwargs=generation_config)
                thread.start()

                for token in streamer:
                    if token:
                        delta = token.replace(user_input, "").strip()
                        full_response += delta
                        if delta:
                            yield json.dumps({
                                "content": delta,
                                "is_end": False
                            }) + "\n"  # 这是修正后的第74行

                yield json.dumps({
                    "content": "[END]",
                    "is_end": True,
                    "metrics": {
                        "time_cost": round(time.time() - start_time, 2),
                        "total_tokens": len(full_response)
                    }
                }) + "\n"

            except Exception as e:
                yield json.dumps({
                    "error": f"生成失败: {str(e)}",
                    "is_end": True
                }) + "\n"
            finally:
                if 'thread' in locals():
                    thread.join(timeout=5)

        return Response(
            stream_with_context(generate()),
            mimetype='application/x-ndjson'
        )

    return bp