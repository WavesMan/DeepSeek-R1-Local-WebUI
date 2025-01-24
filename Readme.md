# DeepSeek-R1-Local-WebUI

**DeepSeek-R1-Local-WebUI** 是一个基于 Flask 的本地模型部署项目，提供了一个交互式的 Web 界面，用于与 **DeepSeek-R1** 模型进行对话。项目支持流式生成响应，并提供了 Light/Dark 主题切换功能。

本项目当前使用的模型是 **DeepSeek-R1 蒸馏 1.5B**，后续会提供更多模型供选择。

---

## 项目功能

- **本地模型部署**：使用 Hugging Face 的 `transformers` 库加载并运行 **DeepSeek-R1** 模型。
- **Web 交互界面**：通过 Flask 提供 Web 服务，用户可以在浏览器中与模型进行对话。
- **流式生成（编写中）**：支持实时流式生成模型响应，提升用户体验。

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
cd DeepSeek-R1
```

#### 2. 安装依赖

双击运行 `install_requirements.bat`，脚本会自动创建虚拟环境并安装依赖。

#### 3. 运行

双击运行 `run.bat`，脚本会自动完成下载模型并启动 Web 服务并打开浏览器。

### Linux/Mac

#### 1. 克隆项目

```bash
git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1
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
3. **流式生成**：流式生成功能依赖于 `TextStreamer`，确保 `transformers` 版本支持该功能。

---

## 贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进项目！如果有任何问题或建议，请通过以下方式联系：

- **GitHub Issues**: [提交 Issue](https://github.com/WavesMan/DeepSeek-R1-Local-WebUI/issues)

---

## 许可证

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