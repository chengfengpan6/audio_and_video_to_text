import os
import sys
import ctypes
import shutil
import time
import html
import threading
import traceback

import av



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
LANGUAGE_OPTIONS = {
    "自动检测 / Auto Detect": None,
    "中文": "zh",
    "English": "en",
}


def get_media_duration(file_path):
    try:
        with av.open(file_path) as container:
            if container.duration is not None:
                return float(container.duration * av.time_base)

            for stream in container.streams:
                if stream.duration is not None and stream.time_base is not None:
                    return float(stream.duration * stream.time_base)
    except Exception as e:
        print(f"⚠️ 无法读取媒体时长: {e}")

    return None


def render_progress_html(percent, status_text, state="idle"):
    safe_percent = max(0.0, min(100.0, float(percent)))
    state_colors = {
        "idle": "#94a3b8",
        "running": "#2563eb",
        "done": "#16a34a",
        "error": "#dc2626",
    }
    bar_color = state_colors.get(state, state_colors["idle"])
    escaped_status = html.escape(status_text)

    return f"""
    <div style="border:1px solid #dbe3ec;border-radius:12px;padding:14px 16px;background:#f8fafc;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-weight:600;color:#0f172a;">
            <span>转录进度</span>
            <span>{safe_percent:.1f}%</span>
        </div>
        <div style="width:100%;height:14px;background:#e2e8f0;border-radius:999px;overflow:hidden;">
            <div style="width:{safe_percent:.1f}%;height:100%;background:{bar_color};transition:width 0.2s linear;"></div>
        </div>
        <div style="margin-top:8px;color:#334155;font-size:14px;line-height:1.4;">{escaped_status}</div>
    </div>
    """


def get_expected_transcribe_seconds(media_duration):
    if not media_duration:
        return 45.0

    return max(18.0, min(90.0, media_duration * 0.18 + 8.0))


def build_progress_message(stage, percent, now, has_actual_progress):
    spinner_frames = ["", ".", "..", "..."]
    spinner = spinner_frames[int(now * 4) % len(spinner_frames)]
    remaining = max(0.0, 100.0 - percent)

    if stage == "copying":
        prefix = f"正在准备文件{spinner}"
    elif stage == "initializing":
        prefix = f"正在初始化模型任务{spinner}"
    elif stage == "transcribing":
        if has_actual_progress:
            prefix = f"正在转录中{spinner}"
        else:
            prefix = f"模型已启动，正在生成首批结果{spinner}"
    elif stage == "saving":
        prefix = f"正在保存结果文件{spinner}"
    elif stage == "done":
        return "转录完成，结果文件已生成。"
    elif stage == "error":
        return "转录失败，请检查控制台或报错信息。"
    else:
        return "等待开始转录..."

    return f"{prefix} 当前进度 {percent:.1f}%，还需等待约 {remaining:.1f}%。"


def estimate_progress_percent(processed_seconds, total_seconds):
    if not total_seconds or total_seconds <= 0:
        return None

    progress = float(processed_seconds / total_seconds) * 100.0
    return max(1.0, min(99.0, progress))


def create_progress_state():
    now = time.time()
    return {
        "lock": threading.Lock(),
        "stage": "idle",
        "stage_updated_at": now,
        "actual_percent": 0.0,
        "progress_updated_at": now,
        "display_percent": 0.0,
        "message": "等待开始转录...",
        "text": "",
        "download": None,
        "error_text": None,
        "done": False,
        "media_duration": None,
        "has_actual_progress": False,
    }


def update_progress_state(state, **kwargs):
    now = time.time()
    with state["lock"]:
        new_stage = kwargs.get("stage")
        if new_stage is not None and new_stage != state["stage"]:
            state["stage"] = new_stage
            state["stage_updated_at"] = now

        if "actual_percent" in kwargs and kwargs["actual_percent"] is not None:
            state["actual_percent"] = float(kwargs["actual_percent"])
            state["progress_updated_at"] = now

        if "message" in kwargs and kwargs["message"] is not None:
            state["message"] = kwargs["message"]

        if "text" in kwargs and kwargs["text"] is not None:
            state["text"] = kwargs["text"]

        if "download" in kwargs and kwargs["download"] is not None:
            state["download"] = kwargs["download"]

        if "error_text" in kwargs and kwargs["error_text"] is not None:
            state["error_text"] = kwargs["error_text"]

        if "done" in kwargs and kwargs["done"] is not None:
            state["done"] = kwargs["done"]

        if "media_duration" in kwargs:
            state["media_duration"] = kwargs["media_duration"]

        if "has_actual_progress" in kwargs and kwargs["has_actual_progress"] is not None:
            state["has_actual_progress"] = kwargs["has_actual_progress"]


def get_progress_snapshot(state):
    with state["lock"]:
        return {
            "stage": state["stage"],
            "stage_updated_at": state["stage_updated_at"],
            "actual_percent": state["actual_percent"],
            "progress_updated_at": state["progress_updated_at"],
            "display_percent": state["display_percent"],
            "message": state["message"],
            "text": state["text"],
            "download": state["download"],
            "error_text": state["error_text"],
            "done": state["done"],
            "media_duration": state["media_duration"],
            "has_actual_progress": state["has_actual_progress"],
        }


def set_display_percent(state, display_percent):
    with state["lock"]:
        state["display_percent"] = float(display_percent)


def compute_target_percent(snapshot, now):
    stage = snapshot["stage"]
    actual_percent = snapshot["actual_percent"]
    stage_elapsed = max(0.0, now - snapshot["stage_updated_at"])

    if stage == "idle":
        return 0.0

    if stage == "copying":
        return max(actual_percent, min(6.0, 1.0 + stage_elapsed * 8.0))

    if stage == "initializing":
        return max(actual_percent, min(12.0, 6.0 + stage_elapsed * 5.0))

    if stage == "transcribing":
        expected_seconds = get_expected_transcribe_seconds(snapshot["media_duration"])
        if stage_elapsed <= expected_seconds:
            estimated = 12.0 + (stage_elapsed / expected_seconds) * 83.0
        else:
            extra_elapsed = stage_elapsed - expected_seconds
            estimated = 95.0 + min(4.0, extra_elapsed / max(12.0, expected_seconds * 0.4) * 4.0)

        return min(99.0, max(actual_percent, estimated))

    if stage == "saving":
        return max(actual_percent, min(99.5, 97.0 + stage_elapsed * 10.0))

    if stage == "done":
        return 100.0

    if stage == "error":
        return actual_percent

    return actual_percent


def advance_display_percent(current_display, target_percent, stage):
    if stage == "done":
        return 100.0

    if target_percent <= current_display:
        if stage == "transcribing" and current_display < 99.0:
            return min(99.0, current_display + 0.15)
        return current_display

    return max(current_display, target_percent)


def get_progress_visual_state(stage):
    if stage == "done":
        return "done"
    if stage == "error":
        return "error"
    if stage == "idle":
        return "idle"
    return "running"


def run_transcription_task(temp_file_path, selected_language_label, state):
    local_file_path = None
    start_time = time.time()

    try:
        file_name = os.path.basename(temp_file_path)
        _, ext = os.path.splitext(file_name)
        safe_name = f"temp_{int(time.time())}{ext}"
        local_file_path = os.path.join(os.getcwd(), safe_name)

        update_progress_state(
            state,
            stage="copying",
            actual_percent=2,
            message="文件已接收，正在复制到本地处理目录...",
        )

        shutil.copy(temp_file_path, local_file_path)
        print(f"\n📂 收到文件: {file_name} -> 正在处理...")

        media_duration = get_media_duration(local_file_path)
        if media_duration:
            initializing_message = f"媒体总时长约 {media_duration:.2f} 秒，正在初始化识别任务..."
        else:
            initializing_message = "正在初始化识别任务，媒体总时长暂时无法读取。"

        update_progress_state(
            state,
            stage="initializing",
            actual_percent=8,
            message=initializing_message,
            media_duration=media_duration,
        )

        update_progress_state(
            state,
            stage="transcribing",
            actual_percent=12,
            message="模型已启动，正在生成首批结果...",
        )

        selected_language = LANGUAGE_OPTIONS.get(selected_language_label)
        transcribe_kwargs = {"beam_size": 5}
        if selected_language is not None:
            transcribe_kwargs["language"] = selected_language

        segments, info = model.transcribe(local_file_path, **transcribe_kwargs)

        full_text_parts = []
        segment_count = 0

        print("🎙️ 正在转录中...", end="")
        for segment in segments:
            print(".", end="", flush=True)
            segment_count += 1
            full_text_parts.append(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n")
            current_text = "".join(full_text_parts)

            progress_percent = estimate_progress_percent(segment.end, media_duration)
            if progress_percent is None:
                progress_percent = min(95.0, 15.0 + segment_count * 3.0)
            else:
                progress_percent = min(95.0, max(15.0, progress_percent))

            update_progress_state(
                state,
                stage="transcribing",
                actual_percent=progress_percent,
                message="正在转录中...",
                text=current_text,
                has_actual_progress=True,
            )
        print(" 完成！")

        original_name_no_ext = os.path.splitext(file_name)[0]
        txt_filename = f"{original_name_no_ext}.txt"
        full_text = "".join(full_text_parts)

        update_progress_state(
            state,
            stage="saving",
            actual_percent=98,
            message="转录已完成，正在保存 TXT 文件...",
            text=full_text,
        )

        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        duration = time.time() - start_time
        info_header = (
            f"✅ 转录完成！耗时: {duration:.2f}秒\n"
            f"选择语言: {selected_language_label}\n"
            f"检测语言: {info.language}\n"
            + "=" * 30
            + "\n\n"
        )

        update_progress_state(
            state,
            stage="done",
            actual_percent=100,
            message="转录完成，结果文件已生成。",
            text=info_header + full_text,
            download=txt_filename,
            done=True,
        )

    except Exception:
        error_text = f"❌ 运行报错:\n{traceback.format_exc()}"
        update_progress_state(
            state,
            stage="error",
            actual_percent=0,
            message="转录失败，请检查控制台或报错信息。",
            error_text=error_text,
            done=True,
        )

    finally:
        if local_file_path and os.path.exists(local_file_path):
            try:
                os.remove(local_file_path)
            except:
                pass
# =======================================

print(f"🚀 正在初始化模型 {MODEL_SIZE}...")
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    print("✅ 模型加载完成！")
except Exception as e:
    print(f"❌ 模型初始化失败: {e}")
    model = None


def transcribe_audio(temp_file_path, selected_language_label):
    # 检查是否为空 (如果用户清空了上传框)
    if temp_file_path is None:
        yield render_progress_html(0, "等待上传文件...", "idle"), "等待上传文件...", None
        return

    if model is None:
        yield render_progress_html(0, "❌ 错误：模型未加载，可能是 DLL 缺失。", "error"), "❌ 错误：模型未加载，可能是 DLL 缺失。", None
        return

    state = create_progress_state()
    worker = threading.Thread(
        target=run_transcription_task,
        args=(temp_file_path, selected_language_label, state),
        daemon=True,
    )
    worker.start()

    last_payload = None

    while True:
        snapshot = get_progress_snapshot(state)
        now = time.time()
        target_percent = compute_target_percent(snapshot, now)
        display_percent = advance_display_percent(
            snapshot["display_percent"],
            target_percent,
            snapshot["stage"],
        )
        set_display_percent(state, display_percent)

        output_text = snapshot["error_text"] or snapshot["text"]
        status_text = snapshot["message"]
        if snapshot["stage"] not in {"done", "error", "idle"}:
            status_text = build_progress_message(
                snapshot["stage"],
                display_percent,
                now,
                snapshot["has_actual_progress"],
            )

        payload = (
            render_progress_html(
                display_percent,
                status_text,
                get_progress_visual_state(snapshot["stage"]),
            ),
            output_text,
            snapshot["download"],
        )

        if payload != last_payload:
            yield payload
            last_payload = payload

        if snapshot["done"] and (snapshot["stage"] == "error" or int(display_percent) >= 100):
            break

        time.sleep(0.2)


# ============================================================
#                      界面 UI 定义
# ============================================================
with gr.Blocks(title="Whisper 本地全能版") as demo:
    gr.Markdown(f"## 🎙️ Whisper 本地转录 ({MODEL_SIZE})")
    gr.Markdown("支持 **MP3, WAV, M4A** 音频及 **MP4, MKV, MOV** 视频格式。拖入文件后，选择语言并点击开始转录。")

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

            language_selector = gr.Dropdown(
                label="🌐 生成文字语言（识别语言）",
                choices=list(LANGUAGE_OPTIONS.keys()),
                value="自动检测 / Auto Detect",
                info="选择音视频的主要语言；中文和英文可手动指定，不确定时可用自动检测。"
            )

            submit_btn = gr.Button("开始转录", variant="primary")

        with gr.Column(scale=2):
            progress_display = gr.HTML(render_progress_html(0, "等待开始转录...", "idle"))
            output_text = gr.TextArea(label="📝 识别结果预览", lines=20)
            download_btn = gr.File(label="💾 下载 TXT 结果")

    # ==================== 交互逻辑 ====================

    # 只保留手动触发，避免“上传自动开始”与“按钮点击开始”重复执行同一任务
    submit_btn.click(
        fn=transcribe_audio,
        inputs=[media_input, language_selector],
        outputs=[progress_display, output_text, download_btn]
    )

if __name__ == "__main__":
    # 启动网页
    demo.queue()
    demo.launch(inbrowser=True)
