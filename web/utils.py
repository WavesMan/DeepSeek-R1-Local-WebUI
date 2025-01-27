# web/utils.py
from flask import Response
from typing import Generator
import time
import html

class WebUtils:
    @staticmethod
    def format_stream_response(text: str, original_input: str) -> str:
        """
        格式化流式响应文本，处理特殊字符和输入文本
        
        参数:
            text (str): 原始生成文本
            original_input (str): 用户输入的原始文本
            
        返回:
            str: 处理后的 HTML 安全文本
        """
        # 移除原始输入文本（如果存在）
        clean_text = text.replace(original_input, "").strip()
        
        # 转义 HTML 特殊字符
        safe_text = html.escape(clean_text)
        
        # 格式化换行和空格（保留前端样式）
        formatted_text = (
            safe_text
            .replace("\n", "<br>")
            .replace(" ", "&nbsp;")
            .replace("\t", "&nbsp;" * 4)
        )
        return formatted_text

    @staticmethod
    def create_stream_response(
        stream_generator: Generator, 
        stream_delay: float = 0.1
    ) -> Response:
        """
        创建 Flask 流式响应
        
        参数:
            stream_generator (Generator): 生成器函数
            stream_delay (float): 流式延迟（秒）
            
        返回:
            Response: Flask 响应对象
        """
        def generate():
            for text_chunk in stream_generator:
                yield f"{text_chunk} "
                time.sleep(stream_delay)
                
        return Response(
            generate(), 
            content_type="text/plain", 
            headers={"X-Content-Type-Options": "nosniff"}
        )

    @staticmethod
    def validate_input(input_text: str, max_length: int = 2000) -> tuple[bool, str]:
        """
        验证用户输入的合法性
        
        参数:
            input_text (str): 用户输入文本
            max_length (int): 允许的最大长度
            
        返回:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        if not input_text.strip():
            return False, "输入不能为空"
        if len(input_text) > max_length:
            return False, f"输入长度超过限制（最大 {max_length} 字符）"
        return True, ""

    @staticmethod
    def log_request(request) -> dict:
        """
        记录请求基本信息
        
        返回:
            dict: 包含客户端信息的字典
        """
        return {
            "method": request.method,
            "endpoint": request.endpoint,
            "remote_addr": request.remote_addr,
            "user_agent": str(request.user_agent)
        }