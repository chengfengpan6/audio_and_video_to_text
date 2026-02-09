[🇺🇸 English](README.md) | [🇨🇳 中文说明](README_zh.md)
<br>

# 🎙️ Whisper Local WebUI - Local AI Audio/Video to Text Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Faster-Whisper](https://img.shields.io/badge/Model-Faster--Whisper-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

This is a localized speech recognition tool built on `faster-whisper` and `Gradio`. It leverages OpenAI's **Large-v3** model with **CUDA GPU acceleration** to quickly and accurately transcribe video or audio files into text (TXT).

**Key Advantages:** Permanently free, unlimited duration, completely offline (privacy protected), and requires no complex environment configuration (includes built-in auto-fix scripts).

---

## ✨ Features

* **⚡ Extreme Performance**: Uses the `faster-whisper` (CTranslate2) engine, 4-5x faster than the original Whisper.
* **🧠 Top-tier Model**: Defaults to the `large-v3` model with `int8_float16` quantization. Runs smoothly on GPUs with 4GB+ VRAM.
* **🖥️ Simple GUI**: Modern Web interface based on Gradio. Supports drag-and-drop upload and automatic transcription.
* **🎞️ All-Format Support**: Supports MP3, WAV, M4A, FLAC audio, and MP4, MKV, MOV video formats.
* **🛠️ Auto-Fix**: Built-in DLL path dynamic loading script ("Nuclear Fix") automatically resolves common Windows issues like missing `cublas64_12.dll` or `zlibwapi.dll`.
* **🖱️ One-Click Start**: Includes a `.bat` script. Double-click to run without using the command line.

---

## 🛠️ Requirements

* **OS**: Windows 10 / 11
* **GPU**: NVIDIA GPU (Recommended VRAM ≥ 4GB)
* **Driver**: CUDA Toolkit 12.x + cuDNN v9
* **Python**: 3.8 or higher

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone [https://github.com/YOUR_USERNAME/whisper-local-webui.git](https://github.com/YOUR_USERNAME/whisper-local-webui.git)
cd whisper-local-webui
```
### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. ⚠️ Crucial Step: Configure DLL Files
**Note:** Due to GitHub file size limits, the core acceleration libraries are NOT included in this repository. You must manually place the following files in the project root directory (same level as `web_ui.py`):

**Required File List:**
1.  **`zlibwapi.dll`** (Download: [WinImage](http://www.winimage.com/zLibDll/zlib123dllx64.zip) or copy from System32)
2.  **NVIDIA cuBLAS Libraries** (Usually found in `venv\Lib\site-packages\nvidia\cublas\bin`):
    * `cublas64_12.dll`
    * `cublasLt64_12.dll`
3.  **NVIDIA cuDNN v9 Libraries** (Usually found in `venv\Lib\site-packages\nvidia\cudnn\bin`):
    * `cudnn_ops64_9.dll`
    * `cudnn_cnn64_9.dll`
    * `cudnn_adv64_9.dll`

> **Tip**: If you have run `pip install`, these NVIDIA DLL files can usually be found in your virtual environment folder `venv/Lib/site-packages/nvidia/`. Please **copy** them to the project root directory.

### 4. Run
Double-click **`run.bat`** in the project directory, or run via command line:
```bash
#find your location
cd /d D:\ 
cd whisper_project
venv\Scripts\activate


python web_ui.py
```
Then, it will automatically open a webpage `http://127.0.0.1:7860`.

---
## 📂 Project Structure

```text
whisper-local-webui/
├── web_ui.py           # [Core] Main program (UI, logic, DLL fix)
├── run.bat             # [Script] Windows one-click start script
├── requirements.txt    # [Config] Python dependencies
├── README.md           # [Doc] English Documentation
├── README_zh.md        # [Doc] Chinese Documentation
├── .gitignore          # [Config] Git ignore rules
└── (DLL Files...)      # [Libs] The .dll files mentioned above
```
## ❓ FAQ

**Q: Why do I get `Library cublas64_12.dll is not found` error?**

A: This is because necessary NVIDIA acceleration library files are missing in the project root. Please strictly follow Step 3 in "Quick Start" and manually copy `zlibwapi.dll`, `cublas`, and `cudnn` related DLL files to the project root directory.

**Q: Why is the first run so slow?**

A: On the first run, the program automatically downloads the `large-v3` model (approx. 3GB) from HuggingFace. The speed depends on your network connection. Subsequent runs will be very fast.

**Q: What if I get "CUDA Out of Memory"?**

A: The default configuration requires about 4GB+ VRAM. If you have less VRAM:
1. Open `web_ui.py`.
2. Change `COMPUTE_TYPE` to `"int8"` (Pure INT8 quantization, lower VRAM usage).
3. Or change `MODEL_SIZE` to `"medium"` or `"small"`.

**Q: Error `TypeError: ... unexpected keyword argument 'show_copy_button'`?**

A: Your Gradio version is too old. Run `pip install --upgrade gradio` to update, or remove the `show_copy_button=True` parameter in the code.

**Q: What if the browser doesn't open automatically?**

A: Please manually copy the address shown in the console (usually `http://127.0.0.1:7860`) and open it in your browser.

## 📜 License
MIT License. See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
* [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
* [Gradio](https://gradio.app/)
* [OpenAI Whisper](https://github.com/openai/whisper)