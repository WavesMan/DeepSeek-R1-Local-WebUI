// static/js/script.js
const chatContainer = document.getElementById('chat-container');
const inputText = document.getElementById('input-text');
const submitBtn = document.getElementById('submit-btn');
const themeToggleBtn = document.getElementById('theme-toggle-btn');

// 添加消息到对话历史
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${role}-message`);

    if (role === 'user') {
        // 用户消息
        messageDiv.textContent = `用户: \n \t${content}`;
    } else {
        // 模型消息
        const header = document.createElement('div');
        header.classList.add('bot-message-header');
        header.textContent = '模型:';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('bot-message-content');

        // 直接展示模型输出的原始内容
        contentDiv.innerHTML = content.replace(/<br>/g, "\n").replace(/&nbsp;/g, " "); // 还原换行和空格
        contentDiv.style.whiteSpace = "pre-wrap"; // 保留换行和空格

        messageDiv.appendChild(header);
        messageDiv.appendChild(contentDiv);
    }

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 自动滚动到底部
}

// 处理用户输入
submitBtn.addEventListener('click', async () => {
    const userInput = inputText.value.trim();
    if (!userInput) return;

    // 清空输入框
    inputText.value = '';

    // 添加用户消息
    addMessage('user', userInput);

    // 发送请求到服务器
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(userInput)}`,
    });

    if (response.ok) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botMessage = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const text = decoder.decode(value);
            botMessage += text;
            addMessage('bot', botMessage); // 实时更新模型消息
        }
    }
});

// 主题切换逻辑
themeToggleBtn.addEventListener('click', () => {
    const body = document.body;
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
    }
});