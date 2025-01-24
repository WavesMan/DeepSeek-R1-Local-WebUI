# webui.py
from flask import Flask, request, render_template, Response, send_from_directory
from model import DeepSeekModel  # 导入模型模块
import torch  # 添加 torch 导入
from transformers import TextStreamer  # 添加 TextStreamer 导入
import time

# 创建 Flask 应用
app = Flask(__name__)

# 初始化模型
print("正在加载模型...")
model = DeepSeekModel()
print("模型加载完成！")

# 定义 favicon 路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 定义主页
@app.route("/")
def home():
    return render_template('index.html')  # 加载 templates/index.html

# 定义生成端点
@app.route("/generate", methods=["POST"])
def generate():
    input_text = request.form["input_text"]

    # 定义流式生成函数
    def generate_stream():
        inputs = model.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(model.device)
        
        # 创建流式输出器
        streamer = TextStreamer(model.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        # 使用流式生成
        with torch.no_grad():
            for output in model.model.generate(
                **inputs,
                pad_token_id=model.tokenizer.eos_token_id,
                max_length=500,
                num_beams=1,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
                do_sample=True,
                streamer=streamer,  # 使用 TextStreamer 对象
            ):
                # 解码生成结果，并移除用户输入的问题
                generated_text = model.tokenizer.decode(output, skip_special_tokens=True)
                if input_text in generated_text:
                    generated_text = generated_text.replace(input_text, "").strip()
                
                # 保留换行和空格
                generated_text = generated_text.replace("\n", "<br>").replace(" ", "&nbsp;")
                yield generated_text + " "  # 实时推送生成结果
                time.sleep(0.1)  # 控制输出速度

    # 返回流式响应
    return Response(generate_stream(), content_type='text/plain')

# 启动 Web 服务
if __name__ == "__main__":
    # 使用 127.0.0.1 而不是 0.0.0.0
    app.run(host="127.0.0.1", port=5000)