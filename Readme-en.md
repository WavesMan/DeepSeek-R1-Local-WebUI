DeepSeek-R1-Local-WebUI
=======================

<div style="text-align:center">
  <a href="Readme.md">简体中文</a> | <a href="Readme-en.md">English</a>
</div>


---

DeepSeek-R1-Local-WebUI is a local model deployment project based on Flask, providing an interactive web interface for conversing with the **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** model. The project supports streaming generation of responses (currently unavailable) and provides a Light/Dark theme switching feature.

* * *

Project features
----------------

*   **Local Model Deployment**: Load and run the **[DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** model using the Hugging Face `transformers` library.
*   **Web Interactive Interface**: Web services are provided through Flask, allowing users to interact with the model in their browsers.
*   Topic Switch: Supports Light/Dark theme switching to enhance user experience.
*   Model Selection: Provides multiple models for users to choose from, adapting to different hardware configurations.

* * *

Project structure
-----------------

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


* * *

Installation and operation
--------------------------

### Windows

#### 1\. Clone project

git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI


#### 2\. Install dependencies

Double-click to run `install_requirements.bat`, the script will automatically create a virtual environment and install dependencies.

#### Run

Double-click to run `run.bat`, the script will automatically complete the download of the model, start the Web service, and open the browser.

### Linux/Mac

#### 1\. Clone project

git clone https://github.com/WavesMan/DeepSeek-R1-Local-WebUI.git
cd DeepSeek-R1-Local-WebUI


#### 2\. Install dependencies

##### Manual installation (Linux/Mac)

python -m venv deepseek_env       # 创建虚拟环境
source deepseek_env/bin/activate  # 激活虚拟环境
pip install -r requirements.txt   # 安装依赖


#### Download the model

Run the following script to download the **DeepSeek-R1** model:

python downloadR1.py

#### Manual start (Linux/Mac)

python webui.py

Access `http://127.0.0.1:5000` to use the WebUI.

* * *

Dependency Description
----------------------

*   Python 3.8+: The project is developed based on Python 3.8.
*   Flask: Used for providing web services.
*   Transformers: Used to load and run the **DeepSeek-R1** model.
*   Torch: A deep learning framework for model inference.
*   FontAwesome: Used for interface icons.

* * *

Caution notices
---------------

1. Model Download: The first run requires downloading the **DeepSeek-R1** model, the file is large, please ensure that the network is stable.
2. **Memory requirements**: The model inference requires a certain amount of GPU memory, and it is recommended to use a GPU that supports CUDA.
3. **Streaming Generation**: The streaming generation feature is currently unavailable and will be supported in future versions.

* * *

Model selection
---------------

| Model Name | Model Type | VRAM | Min GPU |
|-----------------------------------|--------|------------|------------------------------|
| DeepSeek-R1-Distill-Qwen-1.5B     | 1.5B   | 4-6 GB     | GTX 1660 Ti、RTX 2060        |
| DeepSeek-R1-Distill-Qwen-7B       | 7B     | 12-16 GB   | RTX 3060、RTX 3080           |
| DeepSeek-R1-Distill-Llama-8B      | 8B     | 16-20 GB   | RTX 3080 Ti、RTX 3090        |
| DeepSeek-R1-Distill-Qwen-14B      | 14B    | 24-32 GB   | RTX 3090、RTX 4090           |
| DeepSeek-R1-Distill-Qwen-32B      | 32B    | 48-64 GB   | A100、H100                   |
| DeepSeek-R1-Distill-Llama-70B     | 70B    | 80-128 GB  | A100、H100、MI250X           |
* * *

Update log
----------

### v1.0.0 (Initial version)

*   Function:
*   Support local deployment of the **DeepSeek-R1** model.
*   Provide a web interactive interface, allowing users to communicate with the model through a browser.
*   Supports Light/Dark theme switching.
*   Provide multiple models for users to choose from, adapting to different hardware configurations.
*   **Known Issues**:
*   Streaming generation feature is currently unavailable.

* * *

Configuration item description
------------------------------

Users can customize the project configuration by modifying the `config.py` file. The following is a description of the configuration items in the `config.py` file:

| Parameter Name        | Default           | Parameters/parameter ranges can be filled in           | Description                                                                 |
|----------------------|-------------------------|----------------------------|--------------------------------------------------------------------------|
| - `max_length`       | `500`                  | 正整数                     | The maximum length of the generated text.                                                     |
| - `num_beams`        | `1`                    | 正整数                     | Beam Search The number of beams used to control the variety of generated text.                     |
| - `temperature`      | `0.7`                  | 0.0 到 1.0                 | The temperature parameter controls the randomness of the generated text. The smaller the value, the more certain the generated text; The larger the value, the more random it is.|
| - `top_k`            | `50`                   | 正整数                     | The Top-K sampling parameter controls the number of words considered when generating text.                           |
| - `top_p`            | `0.9`                  | 0.0 到 1.0                 | The Top-P sampling parameter controls the cumulative probability threshold when text is generated.                           |
| - `do_sample`        | `True`                 | `True` 或 `False`          | Whether to use sampling to generate text. If it is `False` , greedy search is used.                     |
| - `host`             | `"127.0.0.1"`          | 字符串（IP 地址）          | Specifies the host address of the WebUI service.                                                   |
| - `port`             | `5000`                 | 1024 到 65535              | Specifies the port number of the WebUI service.                                                     |
| - `stream_delay`     | `0.1`                  | 正浮点数                   | The delay time (seconds) of stream generation controls the output speed of generated text。                     |
| `AI_WARNING_MESSAGE` | `"内容由 AI 生成，请仔细甄别"` | 字符串                     | AI generated content prompts displayed on the WebUI.                                  |

* * *

Contribution and feedback
-------------------------

Welcome to submit an Issue or Pull Request to improve the project! If you have any questions or suggestions, please contact us in the following way:

*   GitHub Issues: Submit Issue

* * *

License
-------

This project follows the DeepSeek-R1 [MIT License](DeepSeek-R1_LICENSE) This project is open-source based on the [MIT License](LICENSE).

* * *

Thank you
---------

*   DeepSeek team: Provides the DeepSeek-R1 model.
*   Flask: Provides a lightweight web framework.
*   FontAwesome: Provides icon resources.

* * *

## 赞助

通过成为赞助者来支持这个项目。您的支持有助于保持这个项目的生命力！

| Platform       | Link                                                                 |
|----------------|---------------------------------------------------------------------|
| 💖 爱发电       | [Sponsor on Aifadian](https://afdian.net/a/wavesman)           |
| 💰 支付宝       | [Sponsor on AliPay](https://github.com/WavesMan/Disable-automatic-Windows-update/blob/main/src/AliPay.jpg)    |
| 🎁 微信         | [Sponsor on WeChat](https://github.com/WavesMan/Disable-automatic-Windows-update/blob/main/src/WeChat.png)    |
| ⭐ Patreon     | [Sponsor on Patreon](https://patreon.com/Waves_Man)      |
| 🌟 PayPal      | [Donate via PayPal](https://paypal.me/wavesman)                |


* * *

Hope this `README.md` can help you better showcase the project! If you have any other needs, feel free to supplement or modify at any time!

