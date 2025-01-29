from flask import Blueprint, request, render_template, Response 
from core.model_manager  import ModelManager 
from config import MODEL_CONFIG, GENERATION_CONFIG, STREAM_CONFIG 
import time 
 
def create_routes(model_manager):
    bp = Blueprint('main', __name__)
    
    @bp.route('/') 
    def home():
        return render_template(
            'index.html', 
            AI_WARNING_MESSAGE=MODEL_CONFIG["ai_warning"]
        )
    
    @bp.route("/generate",  methods=["POST"])
    def generate():
        input_text = request.form["input_text"] 
        
        # 准备生成参数 
        generation_params = {
            **GENERATION_CONFIG,
            "pad_token_id": model_manager.tokenizer.eos_token_id, 
            "streamer": model_manager.create_streamer() 
        }
        
        def response_stream():
            start_time = time.time() 
            inputs = model_manager.tokenizer(input_text,  return_tensors="pt").to(model_manager.model.device) 
            
            with torch.no_grad(): 
                outputs = model_manager.model.generate( 
                    **inputs,
                    **generation_params 
                )
                
                # 实时处理输出 
                for token in outputs:
                    decoded = model_manager.tokenizer.decode( 
                        token,
                        skip_special_tokens=True 
                    ).replace(input_text, "").strip()
                    
                    formatted = decoded.replace("\n",  "<br>").replace(" ", "&nbsp;")
                    yield formatted + " "
                    time.sleep(STREAM_CONFIG["stream_delay"]) 
    
            print(f"生成耗时: {time.time()-start_time:.2f}s") 
    
        return Response(response_stream(), content_type='text/plain')
    
    return bp 