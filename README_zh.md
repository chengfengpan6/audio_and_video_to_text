# Whisper Local WebUI - 本地 AI 音视频转文字工具

[English](README.md) | [中文说明](README_zh.md)
<br>

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Faster-Whisper](https://img.shields.io/badge/Model-Faster--Whisper-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

这是一个基于 `faster-whisper` 和 `Gradio` 构建的本地语音识别工具，可以使用 OpenAI Whisper `large-v3` 模型，把音频或视频文件转写成 TXT 文本。

当前 WebUI 支持两种运行方式：适合集显 / 商务本 / 轻薄本的 **CPU 模式**，以及适合 NVIDIA 独显电脑的 **GPU 模式**。即使程序检测到了 NVIDIA 独显，用户也可以手动选择 CPU 模式运行。

**核心优势：** 本地运行、模型下载后可离线使用、支持长文件、浏览器界面操作简单。

---

## 主要功能

* **CPU / GPU 运行模式选择**：转写前先选择整个项目运行在 CPU 还是 NVIDIA CUDA GPU 上。
* **运行模式指示灯**：选中的模式亮绿灯，未选中的模式亮红灯，一眼确认当前是 CPU 还是 GPU。
* **中英文 WebUI**：右上角可用 `ENG/中文` 切换界面语言。
* **识别语言可选**：支持 `自动检测`、`中文`、`English`、`菲律宾语 / Filipino`。
* **上传区显示支持格式**：MP3, WAV, M4A, FLAC, MP4, MKV, MOV。
* **不支持格式提示更清晰**：上传错误格式时只显示 `Unsupported File Format. Click OK to upload again.`
* **转译状态显示**：不再显示不准的百分比进度条，改为动态 `。。。。。`、当前转译时间和音视频总时长。
* **明显的 TXT 下载按钮**：转译完成后点击下载按钮保存 TXT 文档。
* **一键启动**：提供 `run.bat`，双击即可启动本地 WebUI。

---

## 系统要求

* **操作系统**：Windows 10 / 11
* **Python**：3.8 或更高版本
* **CPU 模式**：普通 CPU 即可使用，适合只有集显的笔记本和办公电脑。
* **GPU 模式**：需要 NVIDIA 显卡，并正确配置 CUDA/cuDNN 相关 DLL。
* **磁盘和网络**：首次运行可能需要下载数 GB 的 Whisper 模型文件。

---

## 快速开始

### 1. 克隆或打开项目
```bash
git clone https://github.com/chengfengpan6/audio_and_video_to_text.git
cd audio_and_video_to_text
```

如果你已经有本地项目文件夹，直接打开该文件夹即可。

### 2. 创建并激活虚拟环境
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 可选：配置 GPU DLL 文件
如果你要使用 GPU 模式，需要把 NVIDIA CUDA/cuDNN 运行库放到 `web_ui.py` 同级目录：

1. `zlibwapi.dll`
2. `cublas64_12.dll`
3. `cublasLt64_12.dll`
4. `cudnn_ops64_9.dll`
5. `cudnn_cnn64_9.dll`
6. `cudnn_adv64_9.dll`

这些文件通常可以在下面的目录中找到：

```text
venv\Lib\site-packages\nvidia\cublas\bin
venv\Lib\site-packages\nvidia\cudnn\bin
```

如果你只准备使用 CPU 模式，可以先跳过 GPU 加速配置，启动后在网页里选择 CPU。

### 5. 运行项目
双击 `run.bat`，或者在命令行运行：

```bash
cd /d D:\whisper_project
.\venv\Scripts\activate
python web_ui.py
```

启动后浏览器通常会自动打开：

```text
http://127.0.0.1:7860
```

---

## WebUI 使用流程

1. 在右上角选择 `ENG` 或 `中文`。
2. 在第一步选择运行模式：
   * `CPU`：适合集显电脑、商务本、轻薄本，兼容性最好。
   * `GPU`：适合有 NVIDIA CUDA 独显的电脑，速度更快。
3. 查看 CPU/GPU 指示灯：
   * 绿色表示当前启用。
   * 红色表示当前未启用。
4. 上传支持格式的文件：MP3, WAV, M4A, FLAC, MP4, MKV, MOV。
5. 选择识别语言：`自动检测`、`中文`、`English` 或 `菲律宾语 / Filipino`。
6. 点击“开始转录”。
7. 等待状态区显示动态点点、当前转译时间和音视频总时长。
8. 转译完成后，点击 TXT 下载按钮保存结果。

---

## 模型支持的语言

已从本地 `faster-whisper` tokenizer 确认：当前部署的 Whisper 多语言模型接受 **100 个语言码**。目前 WebUI 手动下拉框提供 `自动检测`、`中文`、`English`、`菲律宾语 / Filipino`；如果要识别其他语言，可以先使用 `自动检测`。如需把某种语言加入手动选择下拉框，可继续在 `web_ui.py` 中扩展语言选项。

| 语言码 | 语言 |
| --- | --- |
| `af` | 南非荷兰语 |
| `am` | 阿姆哈拉语 |
| `ar` | 阿拉伯语 |
| `as` | 阿萨姆语 |
| `az` | 阿塞拜疆语 |
| `ba` | 巴什基尔语 |
| `be` | 白俄罗斯语 |
| `bg` | 保加利亚语 |
| `bn` | 孟加拉语 |
| `bo` | 藏语 |
| `br` | 布列塔尼语 |
| `bs` | 波斯尼亚语 |
| `ca` | 加泰罗尼亚语 |
| `cs` | 捷克语 |
| `cy` | 威尔士语 |
| `da` | 丹麦语 |
| `de` | 德语 |
| `el` | 希腊语 |
| `en` | 英语 |
| `es` | 西班牙语 |
| `et` | 爱沙尼亚语 |
| `eu` | 巴斯克语 |
| `fa` | 波斯语 |
| `fi` | 芬兰语 |
| `fo` | 法罗语 |
| `fr` | 法语 |
| `gl` | 加利西亚语 |
| `gu` | 古吉拉特语 |
| `ha` | 豪萨语 |
| `haw` | 夏威夷语 |
| `he` | 希伯来语 |
| `hi` | 印地语 |
| `hr` | 克罗地亚语 |
| `ht` | 海地克里奥尔语 |
| `hu` | 匈牙利语 |
| `hy` | 亚美尼亚语 |
| `id` | 印度尼西亚语 |
| `is` | 冰岛语 |
| `it` | 意大利语 |
| `ja` | 日语 |
| `jw` | 爪哇语 |
| `ka` | 格鲁吉亚语 |
| `kk` | 哈萨克语 |
| `km` | 高棉语 |
| `kn` | 卡纳达语 |
| `ko` | 韩语 |
| `la` | 拉丁语 |
| `lb` | 卢森堡语 |
| `ln` | 林加拉语 |
| `lo` | 老挝语 |
| `lt` | 立陶宛语 |
| `lv` | 拉脱维亚语 |
| `mg` | 马拉加斯语 |
| `mi` | 毛利语 |
| `mk` | 马其顿语 |
| `ml` | 马拉雅拉姆语 |
| `mn` | 蒙古语 |
| `mr` | 马拉地语 |
| `ms` | 马来语 |
| `mt` | 马耳他语 |
| `my` | 缅甸语 |
| `ne` | 尼泊尔语 |
| `nl` | 荷兰语 |
| `nn` | 新挪威语 |
| `no` | 挪威语 |
| `oc` | 奥克语 |
| `pa` | 旁遮普语 |
| `pl` | 波兰语 |
| `ps` | 普什图语 |
| `pt` | 葡萄牙语 |
| `ro` | 罗马尼亚语 |
| `ru` | 俄语 |
| `sa` | 梵语 |
| `sd` | 信德语 |
| `si` | 僧伽罗语 |
| `sk` | 斯洛伐克语 |
| `sl` | 斯洛文尼亚语 |
| `sn` | 修纳语 |
| `so` | 索马里语 |
| `sq` | 阿尔巴尼亚语 |
| `sr` | 塞尔维亚语 |
| `su` | 巽他语 |
| `sv` | 瑞典语 |
| `sw` | 斯瓦希里语 |
| `ta` | 泰米尔语 |
| `te` | 泰卢固语 |
| `tg` | 塔吉克语 |
| `th` | 泰语 |
| `tk` | 土库曼语 |
| `tl` | 他加禄语 / 菲律宾语 |
| `tr` | 土耳其语 |
| `tt` | 鞑靼语 |
| `uk` | 乌克兰语 |
| `ur` | 乌尔都语 |
| `uz` | 乌兹别克语 |
| `vi` | 越南语 |
| `yi` | 意第绪语 |
| `yo` | 约鲁巴语 |
| `zh` | 中文 |
| `yue` | 粤语 |

---

## 只有集显的轻薄本 / 商务本详细教程

如果你的电脑没有 NVIDIA 独显，只有 Intel Iris Xe、Intel UHD、AMD Radeon 集显，或者是公司办公本、轻薄本，请按下面的 CPU 模式使用。

### 使用前要知道

CPU 模式更兼容，但速度会明显慢于 GPU 模式。`large-v3` 是较大的 AI 模型，首次下载和加载都可能需要较长时间。

建议：

* 插上电源再运行。
* 关闭大型软件，比如游戏、剪辑软件、很多标签页的浏览器。
* 第一次先用 1 到 3 分钟的小音频测试。
* 能上传音频就尽量上传音频，不要直接上传超长视频。
* 如果必须处理长视频，建议先把视频导出为 MP3、WAV、M4A 或 FLAC，再上传音频。
* CPU 模式处理长文件可能比音视频本身时长更久，请不要中途刷新页面。

### 一步一步操作

1. 安装 Python 3.8 或更高版本。
2. 打开 PowerShell，进入项目目录。
3. 创建虚拟环境：
   ```bash
   python -m venv venv
   ```
4. 激活虚拟环境：
   ```bash
   .\venv\Scripts\activate
   ```
5. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
6. 启动 WebUI：
   ```bash
   python web_ui.py
   ```
7. 如果浏览器没有自动打开，手动打开：
   ```text
   http://127.0.0.1:7860
   ```
8. 在第一步运行模式里选择 `CPU（兼容模式 / iGPU 电脑）`。
9. 确认 CPU 灯为绿色，GPU 灯为红色。
10. 上传支持格式的文件。
11. 选择音视频主要语言。不确定时选择 `自动检测 / Auto Detect`。
12. 点击“开始转录”。
13. 等待状态显示完成。
14. 点击“下载 TXT 文档”按钮保存文本结果。

### CPU 模式下推荐的长文件工作流

如果你发现长视频很慢：

1. 先把视频转成音频文件。
2. 推荐格式：MP3、WAV、M4A 或 FLAC。
3. 在 WebUI 中保持 CPU 模式。
4. 上传音频文件开始转写。
5. 不要关闭终端窗口，不要刷新网页，直到转写完成。

---

## 项目结构

```text
whisper-local-webui/
├── web_ui.py           # 主程序：WebUI、运行模式选择、转写逻辑
├── run.bat             # Windows 一键启动脚本
├── requirements.txt    # Python 依赖列表
├── README.md           # 英文文档
├── README_zh.md        # 中文文档
├── .gitignore          # Git 忽略规则
└── (DLL files...)      # 可选 GPU 运行库文件
```

---

## 常见问题

**Q: 没有 NVIDIA 独显可以用吗？**

A: 可以。启动网页后，在第一步选择 `CPU（兼容模式 / iGPU 电脑）`。

**Q: CPU 模式为什么慢？**

A: Whisper `large-v3` 是大模型。CPU 模式主要解决兼容性，不是最快方案。

**Q: 第一次运行为什么慢？**

A: 首次运行可能需要从 Hugging Face 下载模型，并加载到本地。模型缓存后，后续启动会快一些。

**Q: GPU 模式启动失败怎么办？**

A: 先切换到 CPU 模式使用。GPU 模式需要 NVIDIA 显卡和匹配的 CUDA/cuDNN DLL。

**Q: 支持哪些文件格式？**

A: MP3, WAV, M4A, FLAC, MP4, MKV, MOV。

**Q: 上传了不支持的文件会怎样？**

A: 页面会显示 `Unsupported File Format. Click OK to upload again.` 点击 OK 后重新上传支持格式即可。

**Q: 浏览器没有自动打开怎么办？**

A: 手动打开 `http://127.0.0.1:7860`。

---

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。

## 致谢

* [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)
* [Gradio](https://gradio.app/)
* [OpenAI Whisper](https://github.com/openai/whisper)
