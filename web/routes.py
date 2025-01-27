# web/routes.py
from flask import Blueprint, request, render_template, Response
from core.model_manager import ModelManager
from core.generator import TextGenerator
from web.utils import WebUtils
from config import GENERATION_CONFIG, WEBUI_CONFIG, MODEL_CONFIG
import time

# 创建蓝图实例
bp = Blueprint('main', __name__)

# 初始化模型管理器和生成器
model_manager = ModelManager(MODEL_CONFIG["model_path"])
text_generator = TextGenerator(
    model_manager=model_manager,
    generation_config=GENERATION_CONFIG
)

@bp.route('/')
def home():
    """主页路由"""
    return render_template(
        'index.html',
        AI_WARNING_MESSAGE=MODEL_CONFIG["ai_warning"]
    )

@bp.route("/generate", methods=["POST"])
def generate():
    """文本生成端点"""
    input_text = request.form.get("input_text", "")
    
    # 输入验证
    is_valid, error_msg = WebUtils.validate_input(
        input_text,
        max_length=MODEL_CONFIG["input_max_length"]
    )
    if not is_valid:
        return Response(error_msg, status=400, mimetype="text/plain")

    def response_stream():
        """流式生成响应"""
        start_time = time.time()
        
        # 执行生成
        for output in text_generator.generate_stream(input_text):
            # 解码生成结果
            generated_text = model_manager.tokenizer.decode(
                output, 
                skip_special_tokens=True
            )
            
            # 格式化文本
            formatted_text = WebUtils.format_stream_response(
                text=generated_text,
                original_input=input_text
            )
            
            yield formatted_text + " "
        
        # 记录生成耗时
        print(f"Generation completed in {time.time()-start_time:.2f}s")

    # 创建流式响应
    return WebUtils.create_stream_response(
        stream_generator=response_stream(),
        stream_delay=WEBUI_CONFIG["stream_delay"]
    )