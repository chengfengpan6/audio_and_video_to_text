[English](README.md) | [中文说明](README_zh.md)
<br>

# Whisper Local WebUI - Local AI Audio/Video to Text Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Faster-Whisper](https://img.shields.io/badge/Model-Faster--Whisper-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

This is a local speech recognition tool built with `faster-whisper` and `Gradio`. It can transcribe audio or video files into TXT text with the OpenAI Whisper `large-v3` model.

The WebUI now supports both **CPU mode** for iGPU / business laptops and **GPU mode** for NVIDIA dGPU computers. Even if an NVIDIA dGPU is detected, you can still manually choose CPU mode before transcription.

**Key advantages:** free to use, local/offline after the model is downloaded, supports long files, and provides a simple browser-based workflow.

---

## Features

* **CPU or GPU runtime selection**: choose whether the whole project runs on CPU or NVIDIA CUDA GPU before uploading files.
* **Runtime indicator lights**: the selected mode turns green and the unselected mode turns red, so it is clear whether CPU or GPU is active.
* **Bilingual WebUI**: switch the interface language in the top-right corner with `ENG/中文`.
* **Selectable transcription language**: choose `Auto Detect`, `Chinese`, `English`, or `Filipino`.
* **Supported file formats shown in the upload area**: MP3, WAV, M4A, FLAC, MP4, MKV, MOV.
* **Clear unsupported-format handling**: unsupported uploads show `Unsupported File Format. Click OK to upload again.`
* **Live transcription status**: shows animated dots plus current transcription time and media duration instead of an inaccurate percentage bar.
* **Clear TXT download button**: after transcription finishes, use the prominent download button to download the generated TXT file.
* **One-click start script**: `run.bat` starts the local WebUI without typing commands.

---

## Requirements

* **OS**: Windows 10 / 11
* **Python**: 3.8 or higher
* **CPU mode**: works on ordinary CPUs, including laptops with only integrated graphics.
* **GPU mode**: requires an NVIDIA GPU with working CUDA/cuDNN runtime files.
* **Disk/network**: the first model download can be several GB, depending on the Whisper model cache state.

---

## Quick Start

### 1. Clone or open the project
```bash
git clone https://github.com/chengfengpan6/audio_and_video_to_text.git
cd audio_and_video_to_text
```

If you already have this project locally, open its folder directly.

### 2. Create and activate a virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Optional GPU DLL setup
GPU mode needs NVIDIA CUDA/cuDNN libraries. If you want GPU acceleration, place these DLL files in the same folder as `web_ui.py`:

1. `zlibwapi.dll`
2. `cublas64_12.dll`
3. `cublasLt64_12.dll`
4. `cudnn_ops64_9.dll`
5. `cudnn_cnn64_9.dll`
6. `cudnn_adv64_9.dll`

These files are often available under:

```text
venv\Lib\site-packages\nvidia\cublas\bin
venv\Lib\site-packages\nvidia\cudnn\bin
```

CPU-only users can skip GPU acceleration setup and choose CPU mode in the WebUI.

### 5. Run
Double-click `run.bat`, or run:

```bash
cd /d D:\whisper_project
.\venv\Scripts\activate
python web_ui.py
```

The browser should open automatically at:

```text
http://127.0.0.1:7860
```

---

## How to Use the WebUI

1. In the top-right corner, choose `ENG` or `中文` for the WebUI language.
2. In step 1, choose the runtime:
   * `CPU`: best for integrated graphics, business laptops, thin laptops, or maximum compatibility.
   * `GPU`: best for NVIDIA CUDA dGPU computers.
3. Check the CPU/GPU indicator lights:
   * Green means active.
   * Red means inactive.
4. Upload a supported file: MP3, WAV, M4A, FLAC, MP4, MKV, or MOV.
5. Choose the transcription language: `Auto Detect`, `Chinese`, `English`, or `Filipino`.
6. Click `Start Transcription`.
7. Watch the animated status and elapsed time while the model works.
8. When finished, click the download button to save the TXT result.

---

## Supported Languages

Confirmed from the local `faster-whisper` tokenizer, the deployed multilingual Whisper model accepts **100 language codes**. The current WebUI manually exposes `Auto Detect`, `Chinese`, `English`, and `Filipino`; `Auto Detect` can be used for the full multilingual model support listed below.

| Code | Language |
| --- | --- |
| `af` | Afrikaans |
| `am` | Amharic |
| `ar` | Arabic |
| `as` | Assamese |
| `az` | Azerbaijani |
| `ba` | Bashkir |
| `be` | Belarusian |
| `bg` | Bulgarian |
| `bn` | Bengali |
| `bo` | Tibetan |
| `br` | Breton |
| `bs` | Bosnian |
| `ca` | Catalan |
| `cs` | Czech |
| `cy` | Welsh |
| `da` | Danish |
| `de` | German |
| `el` | Greek |
| `en` | English |
| `es` | Spanish |
| `et` | Estonian |
| `eu` | Basque |
| `fa` | Persian |
| `fi` | Finnish |
| `fo` | Faroese |
| `fr` | French |
| `gl` | Galician |
| `gu` | Gujarati |
| `ha` | Hausa |
| `haw` | Hawaiian |
| `he` | Hebrew |
| `hi` | Hindi |
| `hr` | Croatian |
| `ht` | Haitian Creole |
| `hu` | Hungarian |
| `hy` | Armenian |
| `id` | Indonesian |
| `is` | Icelandic |
| `it` | Italian |
| `ja` | Japanese |
| `jw` | Javanese |
| `ka` | Georgian |
| `kk` | Kazakh |
| `km` | Khmer |
| `kn` | Kannada |
| `ko` | Korean |
| `la` | Latin |
| `lb` | Luxembourgish |
| `ln` | Lingala |
| `lo` | Lao |
| `lt` | Lithuanian |
| `lv` | Latvian |
| `mg` | Malagasy |
| `mi` | Maori |
| `mk` | Macedonian |
| `ml` | Malayalam |
| `mn` | Mongolian |
| `mr` | Marathi |
| `ms` | Malay |
| `mt` | Maltese |
| `my` | Burmese |
| `ne` | Nepali |
| `nl` | Dutch |
| `nn` | Norwegian Nynorsk |
| `no` | Norwegian |
| `oc` | Occitan |
| `pa` | Punjabi |
| `pl` | Polish |
| `ps` | Pashto |
| `pt` | Portuguese |
| `ro` | Romanian |
| `ru` | Russian |
| `sa` | Sanskrit |
| `sd` | Sindhi |
| `si` | Sinhala |
| `sk` | Slovak |
| `sl` | Slovenian |
| `sn` | Shona |
| `so` | Somali |
| `sq` | Albanian |
| `sr` | Serbian |
| `su` | Sundanese |
| `sv` | Swedish |
| `sw` | Swahili |
| `ta` | Tamil |
| `te` | Telugu |
| `tg` | Tajik |
| `th` | Thai |
| `tk` | Turkmen |
| `tl` | Tagalog / Filipino |
| `tr` | Turkish |
| `tt` | Tatar |
| `uk` | Ukrainian |
| `ur` | Urdu |
| `uz` | Uzbek |
| `vi` | Vietnamese |
| `yi` | Yiddish |
| `yo` | Yoruba |
| `zh` | Chinese |
| `yue` | Cantonese |

---

## CPU-only Laptop Guide

Use this guide if your laptop has only integrated graphics, such as many thin-and-light laptops, business laptops, Intel Iris Xe laptops, AMD Radeon integrated graphics laptops, or office computers without an NVIDIA dGPU.

### What to expect

CPU mode is more compatible, but it is slower than GPU mode. The first run may also take a long time because the `large-v3` model must be downloaded and loaded.

For best results on CPU-only machines:

* Keep the laptop plugged into power.
* Close heavy apps such as games, video editors, and large browsers.
* Try a short audio file first before processing a long meeting or video.
* Prefer audio files over video files when possible. If you have a video, extracting audio first can reduce workload.
* Be patient with long files. CPU transcription can take much longer than the media duration.

### Step-by-step CPU mode tutorial

1. Install Python 3.8 or newer.
2. Open PowerShell in the project folder.
3. Create the virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate it:
   ```bash
   .\venv\Scripts\activate
   ```
5. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the WebUI:
   ```bash
   python web_ui.py
   ```
7. Open `http://127.0.0.1:7860` if the browser does not open automatically.
8. In the first runtime section, choose `CPU (Compatibility / iGPU)`.
9. Confirm the CPU light is green and GPU is red.
10. Upload a supported file.
11. Choose the transcription language. If unsure, use `Auto Detect`.
12. Click `Start Transcription`.
13. Wait until the status shows completion.
14. Click the TXT download button.

### Recommended CPU workflow

If a long video is slow on CPU:

1. Convert or export the video audio to MP3, WAV, M4A, or FLAC.
2. Upload the audio file instead of the original video.
3. Keep the runtime set to CPU.
4. Let the process finish without refreshing the page.

---

## Project Structure

```text
whisper-local-webui/
├── web_ui.py           # Main WebUI, runtime selection, transcription logic
├── run.bat             # Windows one-click launcher
├── requirements.txt    # Python dependencies
├── README.md           # English documentation
├── README_zh.md        # Chinese documentation
├── .gitignore          # Git ignore rules
└── (DLL files...)      # Optional GPU runtime libraries
```

---

## FAQ

**Q: I do not have an NVIDIA GPU. Can I still use this project?**

A: Yes. Start the WebUI and choose `CPU (Compatibility / iGPU)` in the first step.

**Q: Why is CPU mode slow?**

A: Whisper `large-v3` is a large AI model. CPU mode is designed for compatibility, not maximum speed.

**Q: Why is the first run slow?**

A: The model may need to be downloaded from Hugging Face and loaded locally. Later runs should start faster after the model is cached.

**Q: What should I do if GPU mode fails?**

A: Choose CPU mode first. GPU mode requires an NVIDIA GPU plus compatible CUDA/cuDNN DLL files.

**Q: What file formats are supported?**

A: MP3, WAV, M4A, FLAC, MP4, MKV, and MOV.

**Q: What if I upload an unsupported file?**

A: The WebUI will show `Unsupported File Format. Click OK to upload again.` Click OK, then upload a supported file.

**Q: What if the browser does not open automatically?**

A: Manually open `http://127.0.0.1:7860`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

* [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
* [Gradio](https://gradio.app/)
* [OpenAI Whisper](https://github.com/openai/whisper)
