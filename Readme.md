# DeepSeek-R1-Local-WebUI

<div style="text-align:center">
  <a href="Readme.md">简体中文</a> | <a href="Readme-en.md">English</a>
</div>


---

**DeepSeek-R1-Local-WebUI** 是一个基于 Flask 的本地模型部署项目，提供了一个交互式的 Web 界面，用于与 **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** 模型进行对话。项目支持流式生成响应（暂不可用），并提供了 Light/Dark 主题切换功能。

---

## 项目功能

- **本地模型部署**：使用 Hugging Face 的 `transformers` 库加载并运行 **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** 模型。
- **Web 交互界面**：通过 Flask 提供 Web 服务，用户可以在浏览器中与模型进行对话。
- **主题切换**：支持 Light/Dark 主题切换，提升用户体验。
- **模型选择**：提供多个模型供用户选择，适应不同的硬件配置。

---

## 项目结构

```
DeepSeek-R1
├─ static                    # 静态资源文件
│  ├─ css                    # CSS 样式文件
│  │  └─ styles.css          # 样式表
│  └─ js                     # JavaScript 文件
│     └─ script.js           # 前端交互逻辑
├─ templates                 # HTML 模板文件
│  └─ index.html             # 主页面模板
├─ config.py                 # 配置文件
├─ downloadR1.py             # 模型下载脚本
├─ install_requirements.bat  # 依赖安装脚本（Windows）
├─ model.py                  # 模型加载与推理逻辑
├─ requirements.txt          # Python 依赖列表
├─ run.bat                   # 项目启动脚本（Windows）
└─ webui.py                  # Flask Web 服务入口
```

---

## 安装与运行

### Windows

#### 1. 克隆项目

```bash
git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI
```

#### 2. 安装依赖

双击运行 `install_requirements.bat`，脚本会自动创建虚拟环境并安装依赖。

#### 3. 运行

双击运行 `run.bat`，脚本会自动完成下载模型并启动 Web 服务并打开浏览器。

### Linux/Mac

#### 1. 克隆项目

```bash
git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI
```

#### 2. 安装依赖

##### 手动安装（Linux/Mac）
```bash
python -m venv deepseek_env       # 创建虚拟环境
source deepseek_env/bin/activate  # 激活虚拟环境
pip install -r requirements.txt   # 安装依赖
```

#### 3. 下载模型

运行以下脚本下载 **DeepSeek-R1** 模型：
```bash
python downloadR1.py
```

#### 4. 手动启动（Linux/Mac）
```bash
python webui.py
```
访问 `http://127.0.0.1:5000` 即可使用 WebUI。

---

## 依赖说明

- **Python 3.8+**：项目基于 Python 3.8 开发。
- **Flask**：用于提供 Web 服务。
- **Transformers**：用于加载和运行 **DeepSeek-R1** 模型。
- **Torch**：用于模型推理的深度学习框架。
- **FontAwesome**：用于界面图标。

---

## 注意事项

1. **模型下载**：首次运行需要下载 **DeepSeek-R1** 模型，文件较大，请确保网络畅通。
2. **显存要求**：模型推理需要一定的 GPU 显存，建议使用支持 CUDA 的 GPU。
3. **流式生成**：流式生成功能暂不可用，后续版本将支持。

---

## 模型选择

| 模型名称                          | 参数量 | 显存需求   | 推荐显卡型号（最低）         |
|-----------------------------------|--------|------------|------------------------------|
| DeepSeek-R1-Distill-Qwen-1.5B     | 1.5B   | 4-6 GB     | GTX 1660 Ti、RTX 2060        |
| DeepSeek-R1-Distill-Qwen-7B       | 7B     | 12-16 GB   | RTX 3060、RTX 3080           |
| DeepSeek-R1-Distill-Llama-8B      | 8B     | 16-20 GB   | RTX 3080 Ti、RTX 3090        |
| DeepSeek-R1-Distill-Qwen-14B      | 14B    | 24-32 GB   | RTX 3090、RTX 4090           |
| DeepSeek-R1-Distill-Qwen-32B      | 32B    | 48-64 GB   | A100、H100                   |
| DeepSeek-R1-Distill-Llama-70B     | 70B    | 80-128 GB  | A100、H100、MI250X           |

---

## 更新日志

### v1.0.0 (初始版本)
- **功能**：
  - 支持本地部署 **DeepSeek-R1** 模型。
  - 提供 Web 交互界面，用户可通过浏览器与模型对话。
  - 支持 Light/Dark 主题切换。
  - 提供多个模型供用户选择，适应不同硬件配置。
- **已知问题**：
  - 流式生成功能暂不可用。

---

## 配置项说明

用户可以通过修改 `config.py` 文件来自定义项目的配置。以下是 `config.py` 中的配置项及其说明：

| 参数名               | 默认值                  | 可填参数/参数范围           | 功能说明                                                                 |
|----------------------|-------------------------|----------------------------|--------------------------------------------------------------------------|
| - `max_length`       | `500`                  | 正整数                     | 生成文本的最大长度。                                                     |
| - `num_beams`        | `1`                    | 正整数                     | Beam Search 的 beam 数量，用于控制生成文本的多样性。                     |
| - `temperature`      | `0.7`                  | 0.0 到 1.0                 | 温度参数，控制生成文本的随机性。值越小，生成的文本越确定；值越大，越随机。|
| - `top_k`            | `50`                   | 正整数                     | Top-K 采样参数，控制生成文本时考虑的词汇数量。                           |
| - `top_p`            | `0.9`                  | 0.0 到 1.0                 | Top-P 采样参数，控制生成文本时的累积概率阈值。                           |
| - `do_sample`        | `True`                 | `True` 或 `False`          | 是否使用采样生成文本。若为 `False`，则使用贪婪搜索。                     |
| - `host`             | `"127.0.0.1"`          | 字符串（IP 地址）          | WebUI 服务的主机地址。                                                   |
| - `port`             | `5000`                 | 1024 到 65535              | WebUI 服务的端口号。                                                     |
| - `stream_delay`     | `0.1`                  | 正浮点数                   | 流式生成时的延迟时间（秒），控制生成文本的输出速度。                     |
| `AI_WARNING_MESSAGE` | `"内容由 AI 生成，请仔细甄别"` | 字符串                     | 在 WebUI 中显示的 AI 生成内容提示信息。                                  |

---

## 贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进项目！如果有任何问题或建议，请通过以下方式联系：

- **GitHub Issues**: [提交 Issue](https://github.com/WavesMan/DeepSeek-R1-Local-WebUI/issues)

---

## 许可证

本项目遵循 DeepSeek-R1 的 [MIT 许可证](DeepSeek-R1_LICENSE)
本项目基于 [MIT 许可证](LICENSE) 开源。

---

## 致谢

- **DeepSeek团队**：提供 **DeepSeek-R1** 模型。
- **Flask**：提供轻量级 Web 框架。
- **FontAwesome**：提供图标资源。

---

## 赞助

通过成为赞助者来支持这个项目。您的支持有助于保持这个项目的生命力！

| Platform       | Link                                                                 |
|----------------|---------------------------------------------------------------------|
| 💖 爱发电       | [Sponsor on Aifadian](https://afdian.net/a/wavesman)           |
| 💰 支付宝       | [Sponsor on AliPay](https://github.com/WavesMan/Disable-automatic-Windows-update/blob/main/src/AliPay.jpg)    |
| 🎁 微信         | [Sponsor on WeChat](https://github.com/WavesMan/Disable-automatic-Windows-update/blob/main/src/WeChat.png)    |
| ⭐ Patreon     | [Sponsor on Patreon](https://patreon.com/Waves_Man)      |
| 🌟 PayPal      | [Donate via PayPal](https://paypal.me/wavesman)                |

---

希望这个 `README.md` 能帮助你更好地展示项目！如果有其他需求，欢迎随时补充或修改！