# DeepSeek-R1-Local-WebUI

<div style="text-align:center">
  <a href="Readme.md">简体中文</a> | <a href="Readme-en.md">English</a>
</div>


---

**DeepSeek-R1-Local-WebUI** 是通过Cli控制台启动，基于 Flask 的本地模型部署项目，提供了一个交互式的 Web 界面，用于与 **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** 模型进行对话。项目支持流式生成响应，并提供了 Light/Dark 主题切换功能。

---

## 项目功能

- **Cli控制台** ：通过Cli控制台管理项目。
- **本地模型部署**：使用 Hugging Face 的 `transformers` 库加载并运行 **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** 模型。
- **Web 交互界面**：通过 Flask 提供 Web 服务，用户可以在浏览器中与模型进行对话。
- **主题切换**：支持 Light/Dark 主题切换，提升用户体验。
- **模型选择**：提供多个模型供用户选择，适应不同的硬件配置。

---

## 项目结构

```
DeepSeek-R1-Local-WebUI                 
├─ config                   # 配置项                   
│  ├─ generation.py                     
│  ├─ webui.py                          
│  └─ __init__.py                       
├─ core                     # 核心代码                   
│  ├─ generator.py                      
│  ├─ model_manager.py                  
│  └─ __init__.py                                              
├─ scripts                  # 核心脚本            
│  ├─ memory_monitor.py                 
│  └─ model_downloader.py               
├─ static                   # 静态资源            
│  ├─ css                               
│  │  └─ app.d8079a91.css               
│  └─ js                                
│     ├─ about.ddee9fe6.js              
│     ├─ about.ddee9fe6.js.map          
│     ├─ app.20cd43bb.js                
│     ├─ app.20cd43bb.js.map            
│     ├─ chunk-vendors.28b75eeb.js      
│     └─ chunk-vendors.28b75eeb.js.map  
├─ templates                # 模板文件                
│  └─ index.html                        
├─ web                      # 主程序                   
│  ├─ routes.py                         
│  ├─ utils.py                          
├─ DeepSeek-R1_LICENSE      # DeepSeek-R1 许可证文件
├─ install_dependencies.py  # 安装依赖脚本
├─ LICENSE                  # 许可证文件
├─ Readme-en.md             
├─ Readme.md                
├─ requirements.txt         # 依赖文件
└─ cli.py                   # Cli启动脚本
```

---

## 安装与运行

### 安装前准备

访问 [NVIDIA CUDA Toolkit 12.1 Downloads](https://developer.nvidia.com/cuda-12-1-0-download-archive) 根据您的系统下载安装**CUDA Toolkit 12.1**

### #Windows

#### 手动安装

1. 克隆项目

```bash
git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI
```

2. 安装依赖

```bash
py -m venv deepseek_env              # 创建虚拟环境
.\deepseek_env\Scripts\activate      # 激活虚拟环境
pip install -r cli-require.txt       # 安装依赖
```

3. 运行Cli
```bash
python cli.py                      # 运行Cli
```

3. 访问WebUI
访问 `http://127.0.0.1:5000` 即可使用 WebUI。


### #Linux/Mac

1. 克隆项目

```bash
git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI
```

2. 安装依赖

```bash
python -m venv deepseek_env        # 创建虚拟环境
source deepseek_env/bin/activate   # 激活虚拟环境
pip install -r cli-require.txt     # 安装依赖
```

3. 运行Cli
```bash
python cli.py                      # 运行Cli
```

4. 访问WebUI
访问 `http://127.0.0.1:5000` 即可使用 WebUI。

---

## 依赖说明

- **Python 3.11+**：项目基于 Python 3.11 开发，经测试Python 3.9及以下版本会出现重大错误。**推荐您使用 Python 3.11**。
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
  
### v1.5.0
- **主要改进**
  - 代码重构：优化项目结构，提高可读性和可维护性。
  - UI 改进：提供更现代化的界面交互，增强用户体验。
  - 性能优化：减少资源占用，提高运行效率。
  - 模块化设计：引入更清晰的模块划分，方便功能扩展。
  - 兼容性增强：改进对不同环境的适配性，支持更多平台。

- **重要变更**
  - 配置方式：重构后的 `v1.5.0 版本` 采用新的配置格式
  - API 变更：部分 API 接口有所调整，原有 `v1.0.0 版本` 的用户在迁移时需适配新的 API 规则。

### v1.6.0
- **主要改进**
  - 代码部分重构：优化前后端传导方式为API，提高可维护性。
  - UI 改进：增加了一个“正在生成内容...”UI提示，增强用户体验。
  - 流式传输、生成：支持流式传输、生成，提升用户体验。

### v1.6.1
- **主要改进**
  - 修复存在的BUG
  - 修改`scripts\model_downloader.py`中的依赖下载缺失问题
- **问题解释**
  - 对于 [#3](https://github.com/WavesMan/DeepSeek-R1-Local-WebUI/issues/3) 中的问题，1.5B及其他量化模型（未测试存在哪些模型）由于其量化性质，在长期运行后出现“答非所问”问题是模型问题。出现此问题建议您重新下载模型，并且运行`pip uninstall transformers`后再执行`python scripts\model_downloader.py`重新安装依赖。

### v1.6.2
- **主要改进**
  - 重构前端：采用Vue3+JavaScript+Vite+Pinia实现 


### v1.7.0-1(pre-release)
- **重要更新**
  - 重构启动方式：构建了Cli控制台，简化了项目操作逻辑
  - 添加Cli修改前端访问路径
- **计划更新**
  - Plugin：计划添加插件功能，提升拓展性

---

## 配置项说明

### 1. 基础配置(config/__init__.py)
| 参数名        | 默认值         | 可填参数/参数范围        | 功能说明        |
|---------------|----------------|-----------------------|----------------|
| - `reserved_memory`  | `1`    | 0 - infinite | 预留显存，以防止模型加载失败。 |
| - `input_max_length` | `2000` | 正整数 | 输入文本的最大长度。                |
| - `min_length` | `1` | 正整数  | 生成文本的最小长度。                         |

### 2. 模型配置(config/generation.py)
| 参数名        | 默认值         | 可填参数/参数范围        | 功能说明        |
|---------------|----------------|-----------------------|----------------|
| - `max_length`       | `500`   | 正整数              | 生成文本的最大长度。                                                 |
| - `num_beams`        | `1`     |正整数              | Beam Search 的 beam 数量，用于控制生成文本的多样性。                   |
| - `temperature`      | `0.7`   | 0.0 到 1.0         | 温度参数，控制生成文本的随机性。值越小，生成的文本越确定；值越大，越随机。|
| - `top_k`            | `50`    | 正整数             | Top-K 采样参数，控制生成文本时考虑的词汇数量。                         |
| - `top_p`            | `0.9`     |0.0 到 1.0          |Top-P 采样参数，控制生成文本时的累积概率阈值。                        |  
| - `do_sample`        | `True`  | `True` 或 `False`  | 是否使用采样生成文本。若为 `False`，则使用贪婪搜索。                    |

### 3. WebUI 配置(config/webui.py)
| 参数名        | 默认值         | 可填参数/参数范围        | 功能说明        |
|---------------|----------------|-----------------------|----------------|
| - `host`             | `"127.0.0.1"`          | 字符串（IP 地址）          | WebUI 服务的主机地址。    |
| - `port`             | `5000`                 | 1024 到 65535              | WebUI 服务的端口号。     |

---

## 贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进项目！如果有任何问题或建议，请通过以下方式联系：

- **GitHub Issues**: [提交 Issue](https://github.com/WavesMan/DeepSeek-R1-Local-WebUI/issues)

---

## 许可证

本项目遵循 DeepSeek-R1 的 [MIT 许可证](DeepSeek-R1_LICENSE)
<br>本项目基于 [MIT 许可证](LICENSE) 开源。

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

希望这个 `Readme.md` 能帮助你更好地展示项目！如果有其他需求，欢迎随时补充或修改！
