# web/routes.py
import json
import time
import torch
from transformers import TextIteratorStreamer
from threading import Thread
from core.model_manager import ModelManager
from flask import (
    Blueprint, 
    request, 
    Response, 
    jsonify, 
    render_template,
    stream_with_context  # 新增的关键导入
)


def create_routes(model_manager):
    bp = Blueprint('main', __name__)

    @bp.route('/')
    def index():
        """主入口页面"""
        return render_template(
            'index.html',
            AI_WARNING_MESSAGE="本内容由 AI 生成，仅供参考"
        )

    @bp.route('/api/health')
    def health_check():
        """服务健康检查端点"""
        return jsonify({
            "status": "running",
            "model_loaded": model_manager.model is not None,
            "device": str(model_manager.model.device) if model_manager.model else "none",
            "timestamp": int(time.time())
        })

    @bp.route('/api/chat', methods=['POST'])
    def chat_api():
        """流式聊天处理端点"""
        # 请求内容验证
        if not request.is_json:
            return jsonify({"error": "需要JSON格式请求"}), 415

        data = request.get_json()
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({"error": "输入内容不能为空"}), 400

        def generate():
            """流式生成器"""
            try:
                start_time = time.time()
                full_response = ""
                
                # 创建流式处理器
                streamer = TextIteratorStreamer(
                    model_manager.tokenizer,
                    skip_prompt=True,  # 自动跳过原始提示
                    timeout=60
                )

                # 模型输入处理
                inputs = model_manager.tokenizer(
                    user_input,
                    return_tensors="pt",
                    max_length=2000,
                    truncation=True,
                    padding=True
                ).to(model_manager.model.device)

                # 流式生成配置
                generation_config = {
                    **inputs,
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "do_sample": True,
                    "pad_token_id": model_manager.tokenizer.eos_token_id,
                    "streamer": streamer
                }

                # 启动生成线程
                thread = Thread(target=model_manager.model.generate, kwargs=generation_config)
                thread.start()

                # 流式输出处理
                for token in streamer:
                    if not token:
                        continue
                    # 处理增量内容
                    delta = token.replace(user_input, "").strip()
                    full_response += delta
                    
                    # 发送有效内容块
                    if delta:
                        yield json.dumps({
                            "content": delta,
                            "is_end": False
                        }) + "\n"

                yield json.dumps({
                    "content": "[END]",  # 添加特殊结束标识符
                    "is_end": True,
                    "metrics": {
                        "time_cost": round(time.time() - start_time, 2),
                        "total_tokens": len(full_response)
                    }
                }) + "\n"

            except torch.cuda.OutOfMemoryError as e:
                yield json.dumps({
                    "error": "显存不足，请缩短输入",
                    "is_end": True
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
            stream_with_context(generate()),  # 添加上下文包装器
            mimetype='application/x-ndjson',
            headers={
                'X-Content-Type-Options': 'nosniff',
                'Cache-Control': 'no-cache',
                'Transfer-Encoding': 'chunked'
            }
        )

    return bp
