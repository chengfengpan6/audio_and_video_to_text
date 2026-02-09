# 🎙️ Whisper Local WebUI - 本地 AI 音视频转文字神器

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Faster-Whisper](https://img.shields.io/badge/Model-Faster--Whisper-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

这是一个基于 `faster-whisper` 和 `Gradio` 构建的本地化语音识别工具。它利用 OpenAI 的 **Large-v3** 模型，支持 **CUDA GPU 加速**，能够将视频或音频文件快速、精准地转换为文本（TXT）。

**核心优势：** 永久免费、无限时长、完全离线（保护隐私）、无需配置复杂的环境变量（内置自动修复脚本）。

---

## ✨ 主要功能 (Features)

* **⚡ 极致性能**：使用 `faster-whisper` (CTranslate2) 引擎，比原始 Whisper 快 4-5 倍。
* **🧠 顶级模型**：默认加载 `large-v3` 模型，配合 `int8_float16` 量化，在 4GB+ 显存的显卡上即可流畅运行。
* **🖥️ 简易 GUI**：基于 Gradio 的现代化 Web 界面，支持 MP3/MP4 拖拽上传，自动开始转录。
* **🎞️ 全格式支持**：支持 MP3, WAV, M4A, FLAC 音频及 MP4, MKV, MOV 等视频格式。
* **🛠️ 自动修复**：内置 DLL 路径动态加载脚本 ("Nuclear Fix")，自动解决 Windows 下常见的 `cublas64_12.dll` 和 `zlibwapi.dll` 丢失问题。
* **🖱️ 一键启动**：提供 `.bat` 脚本，双击即可运行，无需输入命令行。

---

## 🛠️ 系统要求 (Requirements)

* **操作系统**: Windows 10 / 11
* **显卡**: NVIDIA 显卡 (建议显存 ≥ 4GB)
* **驱动**: CUDA Toolkit 12.x + cuDNN v9
* **Python**: 3.8 或更高版本

---

## 🚀 快速开始 (Quick Start)

### 1. 克隆项目
```bash
git clone [https://github.com/您的用户名/whisper-local-webui.git](https://github.com/您的用户名/whisper-local-webui.git)
cd whisper-local-webui
```

### 2. 安装依赖
建议使用虚拟环境以避免冲突：
```bash
# 创建虚拟环境
python -m venv venv

# 激活环境
.\venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
```
### 3. ⚠️ 关键步骤：配置 DLL 文件
**注意：** 由于 GitHub 文件大小限制，核心加速库文件未包含在仓库中。您必须将以下文件手动放入项目根目录（即 `web_ui.py` 同级目录）：

**必需文件清单：**
1.  **`zlibwapi.dll`** (下载地址：[WinImage](http://www.winimage.com/zLibDll/zlib123dllx64.zip) 或从 System32 复制)
2.  **NVIDIA cuBLAS 库** (通常在 `venv\Lib\site-packages\nvidia\cublas\bin`):
    * `cublas64_12.dll`
    * `cublasLt64_12.dll`
3.  **NVIDIA cuDNN v9 库** (通常在 `venv\Lib\site-packages\nvidia\cudnn\bin`):
    * `cudnn_ops64_9.dll`
    * `cudnn_cnn64_9.dll`
    * `cudnn_adv64_9.dll`

> **提示**：如果您已运行 `pip install`，这些 NVIDIA DLL 文件通常可以在您的虚拟环境文件夹 `venv/Lib/site-packages/nvidia/` 下找到。请将它们**复制**到项目根目录。


### 4. 运行
双击项目目录下的 **`run.bat`**，或者在命令行运行：
```bash
#找到你自己安装位置
cd /d D:\ 
cd whisper_project
venv\Scripts\activate


python web_ui.py
```
程序启动后，浏览器会自动打开 `http://127.0.0.1:7860`。

---

## 📂 项目结构说明

```text
whisper-local-webui/
├── web_ui.py           # [核心] 主程序，包含 Web 界面、自动转录逻辑和 DLL 修复代码
├── run.bat             # [脚本] Windows 一键启动脚本
├── requirements.txt    # [配置] Python 依赖列表
├── README.md           # [文档] 项目说明书
├── .gitignore          # [配置] Git 忽略规则 (忽略了 venv 和 dll)
└── (DLL Files...)      # [运行库] 上述提到的 .dll 文件需放在这里
```

## ❓ 常见问题 (FAQ)

**Q: 为什么启动时报错 `Library cublas64_12.dll is not found`？**

A: 这是因为项目根目录下缺少必要的 NVIDIA 加速库文件。请务必参考“快速开始”中的第 3 步，将 `zlibwapi.dll`、`cublas` 和 `cudnn` 相关的 DLL 文件手动复制到项目根目录。

**Q: 第一次运行为什么这么慢？**

A: 首次运行时，程序会自动从 HuggingFace 下载 `large-v3` 模型（约 3GB）。下载速度取决于您的网络环境。下载完成后，后续运行会非常快。

**Q: 显存不足 (CUDA Out of Memory) 怎么办？**

A: 默认配置需要约 4GB+ 显存。如果您的显存较小：
1. 打开 `web_ui.py`。
2. 将 `COMPUTE_TYPE` 修改为 `"int8"`（纯 INT8 量化，显存占用更低）。
3. 或者将 `MODEL_SIZE` 修改为 `"medium"` 或 `"small"`。

**Q: 报错 `TypeError: ... unexpected keyword argument 'show_copy_button'`？**

A: 这是因为您的 Gradio 版本过低。请运行 `pip install --upgrade gradio` 更新库，或者在代码中删除 `show_copy_button=True` 参数。

**Q: 网页没有自动弹出怎么办？**

A: 请手动复制控制台显示的地址（通常是 `http://127.0.0.1:7860`）到浏览器中打开。

## 📜 许可证
本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢
* [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
* [Gradio](https://gradio.app/)
* [OpenAI Whisper](https://github.com/openai/whisper)