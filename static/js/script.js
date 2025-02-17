// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const inputField = document.getElementById('input-text');
    const sendButton = document.getElementById('submit-btn');
    let isGenerating = false;
    let loadingIndicator = null;

    // 发送消息
    async function sendMessage() {
        if (isGenerating) return;
        
        const userInput = inputField.value.trim();
        if (!userInput) return;

        isGenerating = true;
        sendButton.disabled = true;
        
        try {
            // 添加用户消息
            addMessage('user', userInput);
            inputField.value = '';
            
            // 创建加载提示
            loadingIndicator = createLoadingIndicator();
            chatContainer.appendChild(loadingIndicator);
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // 创建机器人消息容器
            const botMessageDiv = createBotMessageElement();

            // 发送API请求
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/x-ndjson'
                },
                body: JSON.stringify({ message: userInput })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const chunks = buffer.split('\n');
                
                chunks.slice(0, -1).forEach(chunkStr => {
                    try {
                        const chunk = JSON.parse(chunkStr);
                        if (chunk.error) {
                            updateBotMessage(botMessageDiv, `错误: ${chunk.error}`, true);
                        } else if (chunk.is_end) {
                            finalizeMessage(botMessageDiv, chunk.metrics);
                        } else {
                            appendToMessage(botMessageDiv, chunk.content);
                        }
                    } catch (e) {
                        console.error('解析错误:', e);
                    }
                });
                
                buffer = chunks[chunks.length - 1];
            }

        } catch (error) {
            showError(error.message);
        } finally {
            // 始终移除加载提示
            if (loadingIndicator && loadingIndicator.parentNode) {
                loadingIndicator.remove();
            }
            isGenerating = false;
            sendButton.disabled = false;
        }
    }

    // 添加用户消息
    function addMessage(role, content) {
        const div = document.createElement('div');
        div.className = `message ${role}-message`;
        div.textContent = `${role === 'user' ? '用户: ' : '模型: '}${content}`;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 创建加载提示
    function createLoadingIndicator() {
        const container = document.createElement('div');
        container.className = 'message loading-indicator';
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        
        const text = document.createElement('span');
        text.textContent = '正在生成内容...';
        
        container.append(spinner, text);
        return container;
    }

    // 创建机器人消息元素
    function createBotMessageElement() {
        const container = document.createElement('div');
        container.className = 'message bot-message';
        
        const header = document.createElement('div');
        header.className = 'bot-message-header';
        header.textContent = '模型:';
        
        const content = document.createElement('div');
        content.className = 'bot-message-content';
        
        container.append(header, content);
        chatContainer.appendChild(container);
        return { container, content };
    }

    // 追加消息内容
    function appendToMessage(container, text) {
        const textNode = document.createTextNode(text);
        container.content.appendChild(textNode);
        
        // 触发浏览器重绘以确保实时显示
        void container.content.offsetHeight;
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 完成处理
    function finalizeMessage(container, metrics) {
        // 移除加载提示
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.remove();
        }
        const time = metrics ? metrics.time_cost.toFixed(2) : '未知';
        console.log(`生成完成，耗时: ${time}秒`);
        container.container.classList.add('complete');
    }

    // 错误处理
    function showError(message) {
        // 移除加载提示
        if (loadingIndicator && loadingIndicator.parentNode) {
            loadingIndicator.remove();
        }
        const errDiv = document.createElement('div');
        errDiv.className = 'error-message';
        errDiv.textContent = `错误: ${message}`;
        chatContainer.appendChild(errDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 事件监听
    sendButton.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
