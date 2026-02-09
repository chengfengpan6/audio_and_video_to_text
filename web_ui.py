import os
import sys
import ctypes
import shutil
import time



def nuclear_fix():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["PATH"] = current_dir + ";" + os.environ["PATH"]
    if os.name == 'nt':
        try:
            os.add_dll_directory(current_dir)
        except:
            pass

    dlls_to_preload = [
        "zlibwapi.dll", "cublas64_12.dll", "cublasLt64_12.dll",
        "cudnn_ops64_9.dll", "cudnn_cnn64_9.dll", "cudnn_adv64_9.dll"
    ]

    print("\n🔄 正在预加载核心 DLL (cuDNN v9)...")
    for dll in dlls_to_preload:
        dll_path = os.path.join(current_dir, dll)
        if os.path.exists(dll_path):
            try:
                ctypes.CDLL(dll_path)
            except:
                pass


# 立即执行修复
nuclear_fix()
# ====================================================================

import gradio as gr
from faster_whisper import WhisperModel

# ================= 配置 =================
MODEL_SIZE = "large-v3"
DEVICE = "cuda"
COMPUTE_TYPE = "int8_float16"
# =======================================

print(f"🚀 正在初始化模型 {MODEL_SIZE}...")
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    print("✅ 模型加载完成！")
except Exception as e:
    print(f"❌ 模型初始化失败: {e}")
    model = None


def transcribe_audio(temp_file_path):
    # 检查是否为空 (如果用户清空了上传框)
    if temp_file_path is None:
        return "等待上传文件...", None

    if model is None:
        return "❌ 错误：模型未加载，可能是 DLL 缺失。", None

    # 修复权限问题：复制到本地安全路径
    try:
        file_name = os.path.basename(temp_file_path)
        # 获取文件后缀名
        _, ext = os.path.splitext(file_name)
        # 构造一个安全的文件名，保留原始后缀 (这对 FFmpeg 识别格式很重要)
        safe_name = f"temp_{int(time.time())}{ext}"
        local_file_path = os.path.join(os.getcwd(), safe_name)

        shutil.copy(temp_file_path, local_file_path)
        print(f"\n📂 收到文件: {file_name} -> 正在处理...")
    except Exception as e:
        return f"❌ 文件复制失败: {e}", None

    start_time = time.time()

    try:
        # 开始转录 (faster-whisper 内部会自动处理 mp3 或 mp4)
        segments, info = model.transcribe(local_file_path, beam_size=5, language="zh")

        full_text = ""
        print("🎙️ 正在转录中...", end="")
        for segment in segments:
            print(".", end="", flush=True)
            full_text += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
        print(" 完成！")

        # 保存结果 (使用原文件名 + .txt)
        # 去掉原文件后缀，加上 .txt
        original_name_no_ext = os.path.splitext(file_name)[0]
        txt_filename = f"{original_name_no_ext}.txt"

        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        end_time = time.time()
        duration = end_time - start_time

        # 在文本框最上方添加耗时信息
        info_header = f"✅ 转录完成！耗时: {duration:.2f}秒\n检测语言: {info.language}\n" + "=" * 30 + "\n\n"
        return info_header + full_text, txt_filename

    except Exception as e:
        import traceback
        return f"❌ 运行报错:\n{traceback.format_exc()}", None

    finally:
        # 清理临时文件
        if os.path.exists(local_file_path):
            try:
                os.remove(local_file_path)
            except:
                pass


# ============================================================
#                      界面 UI 定义
# ============================================================
with gr.Blocks(title="Whisper 本地全能版") as demo:
    gr.Markdown(f"## 🎙️ Whisper 本地转录 ({MODEL_SIZE})")
    gr.Markdown("支持 **MP3, WAV, M4A** 音频及 **MP4, MKV, MOV** 视频格式。拖入文件即可自动开始。")

    with gr.Row():
        with gr.Column(scale=1):
            # 1. 改用 File 组件，支持任意格式拖拽
            # file_types 限制了可选文件的类型，提升体验
            media_input = gr.File(
                label="📁 请将 音频 或 视频 文件拖拽到此处",
                type="filepath",
                file_types=[".mp3", ".wav", ".m4a", ".mp4", ".mkv", ".mov", ".flac"],
                height=100
            )

            # 保留按钮，以防自动触发失败，或者用户想重新跑
            submit_btn = gr.Button("手动点击开始转录", variant="primary")

        with gr.Column(scale=2):
            output_text = gr.TextArea(label="📝 识别结果预览", lines=20)
            download_btn = gr.File(label="💾 下载 TXT 结果")

    # ==================== 交互逻辑 ====================

    # 逻辑 A: 点击按钮触发
    submit_btn.click(
        fn=transcribe_audio,
        inputs=media_input,
        outputs=[output_text, download_btn]
    )

    # 逻辑 B: 【新增】文件上传完成后，自动触发转录
    # 这样S一拖进去，松手，它就开始跑了
    media_input.upload(
        fn=transcribe_audio,
        inputs=media_input,
        outputs=[output_text, download_btn]
    )

if __name__ == "__main__":
    # 启动网页
    demo.launch(inbrowser=True)