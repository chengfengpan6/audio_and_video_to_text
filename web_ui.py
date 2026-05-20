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
import ctranslate2
from faster_whisper import WhisperModel

# ================= 配置 =================
MODEL_SIZE = "large-v3"
DEVICE_PROFILES = {
    "cpu": {
        "device": "cpu",
        "compute_type": "int8",
    },
    "gpu": {
        "device": "cuda",
        "compute_type": "int8_float16",
    },
}
UI_LANGUAGE_OPTIONS = ["中文", "ENG"]
DEFAULT_UI_LANGUAGE = "中文"
DEFAULT_BROWSER_PREFS = {
    "ui_language": DEFAULT_UI_LANGUAGE,
    "runtime": None,
    "transcription_language": "auto",
}
ALLOWED_MEDIA_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".mkv", ".mov", ".flac"}
TRANSCRIPTION_LANGUAGE_OPTIONS = {
    "auto": {"code": None, "zh": "自动检测 / Auto Detect", "en": "Auto Detect"},
    "zh": {"code": "zh", "zh": "中文", "en": "Chinese"},
    "en": {"code": "en", "zh": "English", "en": "English"},
    "tl": {"code": "tl", "zh": "菲律宾语 / Filipino", "en": "Filipino"},
}
TEXTS = {
    "中文": {
        "app_title": f"## 🎙️ Whisper 本地转录 ({MODEL_SIZE})",
        "intro": "第一步先选择 **CPU 或 GPU** 运行模式；之后拖入文件、选择语言并点击开始转录。",
        "runtime_label": "① 选择整套项目运行模式",
        "runtime_info": "CPU 适合核显或兼容模式；GPU 适合 NVIDIA CUDA 独显加速。检测到独显时也可以选择 CPU。",
        "cpu_option": "CPU（兼容模式 / iGPU 电脑）",
        "gpu_option": "GPU（CUDA 加速 / dGPU 电脑）",
        "runtime_status_title": "运行模式",
        "gpu_detected": "已检测到 NVIDIA CUDA GPU",
        "gpu_not_detected": "未检测到可用 NVIDIA CUDA GPU",
        "manual_cpu": "即使检测到独显，也可以手动选择 CPU。",
        "choose_runtime": "请先选择运行模式，再上传文件并开始转录。",
        "gpu_unavailable": "当前选择：GPU，但未检测到可用 NVIDIA CUDA GPU。请改选 CPU 兼容模式。",
        "runtime_selected": "当前选择：{runtime_label}。模型将在首次转录时加载到 {device}，计算类型为 {compute_type}。",
        "cpu_light": "CPU",
        "gpu_light": "GPU",
        "active": "运行中",
        "inactive": "未启用",
        "file_label": "② 请将 音频 或 视频 文件拖拽到此处",
        "file_hint": "支持格式：MP3, WAV, M4A, FLAC, MP4, MKV, MOV",
        "language_label": "③ 生成文字语言（识别语言）",
        "language_info": "选择音视频的主要语言；中文、英文和菲律宾语可手动指定，不确定时可用自动检测。",
        "submit": "开始转录",
        "progress_title": "转译状态",
        "progress_idle": "等待开始转录...",
        "elapsed_label": "当前转译时间",
        "media_duration_label": "音视频总时长",
        "total_elapsed_label": "整个转译时间",
        "unknown_time": "读取中",
        "output_label": "📝 识别结果预览",
        "download_label": "⬇ 下载 TXT 文档",
        "missing_file": "等待上传文件...",
        "missing_runtime": "请先在第一步选择 CPU 或 GPU 运行模式。",
        "copying": "文件已接收，正在复制到本地处理目录...",
        "duration_found": "媒体总时长约 {duration:.2f} 秒，正在初始化识别任务...",
        "duration_unknown": "正在初始化识别任务，媒体总时长暂时无法读取。",
        "preparing_runtime": "{message} 正在准备运行模式...",
        "model_started": "模型已启动，正在生成首批结果...",
        "transcribing": "正在转录中...",
        "saving_result": "转录已完成，正在保存 TXT 文件...",
        "done_message": "转录完成，结果文件已生成。",
        "error_message": "转录失败，请检查控制台或报错信息。",
        "done_header": "✅ 转录完成！耗时: {duration:.2f}秒\n运行模式: {runtime_label}\n计算设备: {device} / {compute_type}\n选择语言: {language_label}\n检测语言: {detected_language}\n",
        "runtime_cuda_error": "未检测到可用 NVIDIA CUDA GPU。请返回第一步选择 CPU 兼容模式。",
        "copying_progress": "正在准备文件{spinner}",
        "initializing_progress": "正在初始化模型任务{spinner}",
        "transcribing_progress": "正在转录中{spinner}",
        "first_results_progress": "模型已启动，正在生成首批结果{spinner}",
        "saving_progress": "正在保存结果文件{spinner}",
        "progress_message": "{prefix}",
        "invalid_file_title": "Unsupported File Format",
        "invalid_file_body": "Unsupported File Format. Click OK to upload again.",
        "acknowledge": "OK",
    },
    "ENG": {
        "app_title": f"## 🎙️ Whisper Local Transcription ({MODEL_SIZE})",
        "intro": "First choose whether the whole project runs on **CPU or GPU**. Then upload a file, choose the speech language, and start transcription.",
        "runtime_label": "① Choose project runtime",
        "runtime_info": "CPU is best for iGPU or compatibility mode. GPU uses NVIDIA CUDA acceleration. You can still choose CPU even when a dGPU is detected.",
        "cpu_option": "CPU (Compatibility / iGPU)",
        "gpu_option": "GPU (CUDA acceleration / dGPU)",
        "runtime_status_title": "Runtime Mode",
        "gpu_detected": "NVIDIA CUDA GPU detected",
        "gpu_not_detected": "No available NVIDIA CUDA GPU detected",
        "manual_cpu": "You can still choose CPU even when a dGPU is detected.",
        "choose_runtime": "Please choose a runtime mode before uploading a file and starting transcription.",
        "gpu_unavailable": "GPU is selected, but no available NVIDIA CUDA GPU was detected. Please choose CPU compatibility mode.",
        "runtime_selected": "Selected: {runtime_label}. The model will load on {device} with compute type {compute_type} on first transcription.",
        "cpu_light": "CPU",
        "gpu_light": "GPU",
        "active": "Active",
        "inactive": "Inactive",
        "file_label": "② Drop an audio or video file here",
        "file_hint": "Supported formats: MP3, WAV, M4A, FLAC, MP4, MKV, MOV",
        "language_label": "③ Speech language",
        "language_info": "Choose the main language in the media. Chinese, English, and Filipino can be set manually; use Auto Detect when unsure.",
        "submit": "Start Transcription",
        "progress_title": "Transcription Status",
        "progress_idle": "Waiting to start...",
        "elapsed_label": "Current transcription time",
        "media_duration_label": "Media duration",
        "total_elapsed_label": "Total transcription time",
        "unknown_time": "Reading",
        "output_label": "📝 Transcript Preview",
        "download_label": "⬇ Download TXT Document",
        "missing_file": "Waiting for a file upload...",
        "missing_runtime": "Please choose CPU or GPU runtime mode in step one.",
        "copying": "File received. Copying it into the local processing folder...",
        "duration_found": "Media duration is about {duration:.2f} seconds. Initializing transcription...",
        "duration_unknown": "Initializing transcription. Media duration could not be read yet.",
        "preparing_runtime": "{message} Preparing runtime mode...",
        "model_started": "Model started. Generating the first results...",
        "transcribing": "Transcribing...",
        "saving_result": "Transcription finished. Saving TXT file...",
        "done_message": "Transcription complete. Result file generated.",
        "error_message": "Transcription failed. Please check the console or error message.",
        "done_header": "✅ Transcription complete! Time: {duration:.2f}s\nRuntime: {runtime_label}\nCompute device: {device} / {compute_type}\nSelected language: {language_label}\nDetected language: {detected_language}\n",
        "runtime_cuda_error": "No available NVIDIA CUDA GPU was detected. Please return to step one and choose CPU compatibility mode.",
        "copying_progress": "Preparing file{spinner}",
        "initializing_progress": "Initializing model task{spinner}",
        "transcribing_progress": "Transcribing{spinner}",
        "first_results_progress": "Model started, generating first results{spinner}",
        "saving_progress": "Saving result file{spinner}",
        "progress_message": "{prefix}",
        "invalid_file_title": "Unsupported File Format",
        "invalid_file_body": "Unsupported File Format. Click OK to upload again.",
        "acknowledge": "OK",
    },
}
MODEL_CACHE = {}
MODEL_LOCK = threading.Lock()


def get_cuda_device_count():
    try:
        return ctranslate2.get_cuda_device_count()
    except Exception as e:
        print(f"⚠️ 无法检测 CUDA 设备: {e}")
        return 0


def normalize_ui_language(ui_language):
    if ui_language in UI_LANGUAGE_OPTIONS:
        return ui_language
    return DEFAULT_UI_LANGUAGE


def normalize_runtime(runtime_key):
    legacy_map = {
        "CPU（兼容模式 / iGPU 电脑）": "cpu",
        "GPU（CUDA 加速 / dGPU 电脑）": "gpu",
        "CPU (Compatibility / iGPU)": "cpu",
        "GPU (CUDA acceleration / dGPU)": "gpu",
    }
    runtime_key = legacy_map.get(runtime_key, runtime_key)
    return runtime_key if runtime_key in DEVICE_PROFILES else None


def normalize_transcription_language(language_key):
    legacy_map = {
        "自动检测 / Auto Detect": "auto",
        "Auto Detect": "auto",
        "中文": "zh",
        "Chinese": "zh",
        "English": "en",
        "菲律宾语 / Filipino": "tl",
        "Filipino": "tl",
    }
    language_key = legacy_map.get(language_key, language_key)
    return language_key if language_key in TRANSCRIPTION_LANGUAGE_OPTIONS else "auto"


def t(ui_language, key):
    return TEXTS[normalize_ui_language(ui_language)][key]


def get_runtime_choices(ui_language):
    ui_language = normalize_ui_language(ui_language)
    return [
        (t(ui_language, "cpu_option"), "cpu"),
        (t(ui_language, "gpu_option"), "gpu"),
    ]


def get_runtime_label(runtime_key, ui_language):
    runtime_key = normalize_runtime(runtime_key)
    labels = dict(get_runtime_choices(ui_language))
    reverse_labels = {value: label for label, value in labels.items()}
    return reverse_labels.get(runtime_key, "")


def get_runtime_component_value(runtime_key, ui_language):
    runtime_key = normalize_runtime(runtime_key)
    return runtime_key


def get_transcription_language_choices(ui_language):
    label_key = "zh" if normalize_ui_language(ui_language) == "中文" else "en"
    return [
        (config[label_key], language_key)
        for language_key, config in TRANSCRIPTION_LANGUAGE_OPTIONS.items()
    ]


def get_transcription_language_label(language_key, ui_language):
    language_key = normalize_transcription_language(language_key)
    labels = dict(get_transcription_language_choices(ui_language))
    reverse_labels = {value: label for label, value in labels.items()}
    return reverse_labels.get(language_key, "")


def get_transcription_language_component_value(language_key, ui_language):
    return normalize_transcription_language(language_key)


def get_browser_preferences(ui_language, runtime_key, language_key):
    return {
        "ui_language": normalize_ui_language(ui_language),
        "runtime": normalize_runtime(runtime_key),
        "transcription_language": normalize_transcription_language(language_key),
    }


def is_allowed_media_file(file_path):
    if not file_path:
        return True
    _, ext = os.path.splitext(file_path)
    return ext.lower() in ALLOWED_MEDIA_EXTENSIONS


def render_runtime_status_html(selected_runtime_label, ui_language=DEFAULT_UI_LANGUAGE):
    ui_language = normalize_ui_language(ui_language)
    selected_runtime_label = normalize_runtime(selected_runtime_label)
    cuda_count = get_cuda_device_count()
    gpu_detected_text = t(ui_language, "gpu_detected") if cuda_count > 0 else t(ui_language, "gpu_not_detected")
    selected_text = t(ui_language, "choose_runtime")
    status_color = "#475569"
    cpu_color = "#94a3b8"
    gpu_color = "#94a3b8"
    cpu_state = t(ui_language, "inactive")
    gpu_state = t(ui_language, "inactive")

    if selected_runtime_label in DEVICE_PROFILES:
        profile = DEVICE_PROFILES[selected_runtime_label]
        if profile["device"] == "cuda" and cuda_count < 1:
            selected_text = t(ui_language, "gpu_unavailable")
            status_color = "#b45309"
        else:
            selected_text = t(ui_language, "runtime_selected").format(
                runtime_label=get_runtime_label(selected_runtime_label, ui_language),
                device=profile["device"].upper(),
                compute_type=profile["compute_type"],
            )
            status_color = "#166534"

        if selected_runtime_label == "cpu":
            cpu_color = "#16a34a"
            gpu_color = "#dc2626"
            cpu_state = t(ui_language, "active")
        elif selected_runtime_label == "gpu":
            cpu_color = "#dc2626"
            gpu_color = "#16a34a"
            gpu_state = t(ui_language, "active")

    if ui_language == "中文":
        cuda_line = f"{gpu_detected_text}（CUDA: {cuda_count}）。{t(ui_language, 'manual_cpu')}"
    else:
        cuda_line = f"{gpu_detected_text} (CUDA: {cuda_count}). {t(ui_language, 'manual_cpu')}"

    return f"""
    <div style="border:1px solid #dbe3ec;border-radius:10px;padding:12px 14px;background:#f8fafc;color:#0f172a;line-height:1.55;">
        <div style="font-weight:700;margin-bottom:8px;">{html.escape(t(ui_language, "runtime_status_title"))}</div>
        <div style="display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap;">
            <div style="border:1px solid {cpu_color};border-radius:8px;padding:8px 10px;min-width:120px;background:#ffffff;">
                <span style="display:inline-block;width:12px;height:12px;border-radius:999px;background:{cpu_color};box-shadow:0 0 0 3px color-mix(in srgb, {cpu_color} 18%, transparent);margin-right:8px;"></span>
                <strong>{html.escape(t(ui_language, "cpu_light"))}</strong>
                <span style="color:{cpu_color};margin-left:6px;">{html.escape(cpu_state)}</span>
            </div>
            <div style="border:1px solid {gpu_color};border-radius:8px;padding:8px 10px;min-width:120px;background:#ffffff;">
                <span style="display:inline-block;width:12px;height:12px;border-radius:999px;background:{gpu_color};box-shadow:0 0 0 3px color-mix(in srgb, {gpu_color} 18%, transparent);margin-right:8px;"></span>
                <strong>{html.escape(t(ui_language, "gpu_light"))}</strong>
                <span style="color:{gpu_color};margin-left:6px;">{html.escape(gpu_state)}</span>
            </div>
        </div>
        <div>{html.escape(cuda_line)}</div>
        <div style="margin-top:6px;color:{status_color};">{html.escape(selected_text)}</div>
    </div>
    """


def get_model_for_runtime(selected_runtime_label, ui_language=DEFAULT_UI_LANGUAGE):
    selected_runtime_label = normalize_runtime(selected_runtime_label)
    profile = DEVICE_PROFILES.get(selected_runtime_label)
    if profile is None:
        raise ValueError(t(ui_language, "missing_runtime"))

    if profile["device"] == "cuda" and get_cuda_device_count() < 1:
        raise RuntimeError(t(ui_language, "runtime_cuda_error"))

    cache_key = (MODEL_SIZE, profile["device"], profile["compute_type"])
    with MODEL_LOCK:
        cached_model = MODEL_CACHE.get(cache_key)
        if cached_model is not None:
            return cached_model, profile

        print(
            f"🚀 正在初始化模型 {MODEL_SIZE} "
            f"({profile['device']}, {profile['compute_type']})..."
        )
        loaded_model = WhisperModel(
            MODEL_SIZE,
            device=profile["device"],
            compute_type=profile["compute_type"],
        )
        MODEL_CACHE[cache_key] = loaded_model
        print("✅ 模型加载完成！")
        return loaded_model, profile


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


def format_duration(seconds):
    if seconds is None:
        return None
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def render_progress_html(
    status_text,
    state="idle",
    ui_language=DEFAULT_UI_LANGUAGE,
    elapsed_seconds=0,
    media_duration=None,
    total_elapsed=None,
):
    ui_language = normalize_ui_language(ui_language)
    state_colors = {
        "idle": "#94a3b8",
        "running": "#2563eb",
        "done": "#16a34a",
        "error": "#dc2626",
    }
    accent_color = state_colors.get(state, state_colors["idle"])
    escaped_status = html.escape(status_text)
    elapsed_text = format_duration(elapsed_seconds) or "00:00"
    media_duration_text = format_duration(media_duration) or t(ui_language, "unknown_time")
    total_elapsed_text = format_duration(total_elapsed) or elapsed_text
    secondary_label = t(ui_language, "total_elapsed_label") if state == "done" else t(ui_language, "media_duration_label")
    secondary_value = total_elapsed_text if state == "done" else media_duration_text

    return f"""
    <div style="border:1px solid #dbe3ec;border-radius:12px;padding:14px 16px;background:#f8fafc;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-weight:600;color:#0f172a;">
            <span>{html.escape(t(ui_language, "progress_title"))}</span>
            <span style="color:{accent_color};">{html.escape(elapsed_text)}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:10px;">
            <div style="border:1px solid #e2e8f0;background:#ffffff;border-radius:8px;padding:10px;">
                <div style="font-size:12px;color:#64748b;">{html.escape(t(ui_language, "elapsed_label"))}</div>
                <div style="font-size:22px;font-weight:700;color:#0f172a;line-height:1.2;">{html.escape(elapsed_text)}</div>
            </div>
            <div style="border:1px solid #e2e8f0;background:#ffffff;border-radius:8px;padding:10px;">
                <div style="font-size:12px;color:#64748b;">{html.escape(secondary_label)}</div>
                <div style="font-size:22px;font-weight:700;color:#0f172a;line-height:1.2;">{html.escape(secondary_value)}</div>
            </div>
        </div>
        <div style="border-left:4px solid {accent_color};padding:8px 10px;background:#ffffff;color:#334155;font-size:15px;line-height:1.45;">{escaped_status}</div>
    </div>
    """


def get_expected_transcribe_seconds(media_duration):
    if not media_duration:
        return 45.0

    return max(18.0, min(90.0, media_duration * 0.18 + 8.0))


def build_progress_message(stage, now, has_actual_progress, ui_language=DEFAULT_UI_LANGUAGE):
    ui_language = normalize_ui_language(ui_language)
    spinner_frames = ["。", "。。", "。。。", "。。。。", "。。。。。"]
    spinner = spinner_frames[int(now * 3) % len(spinner_frames)]

    if stage == "copying":
        prefix = t(ui_language, "copying_progress").format(spinner=spinner)
    elif stage == "initializing":
        prefix = t(ui_language, "initializing_progress").format(spinner=spinner)
    elif stage == "transcribing":
        if has_actual_progress:
            prefix = t(ui_language, "transcribing_progress").format(spinner=spinner)
        else:
            prefix = t(ui_language, "first_results_progress").format(spinner=spinner)
    elif stage == "saving":
        prefix = t(ui_language, "saving_progress").format(spinner=spinner)
    elif stage == "done":
        return t(ui_language, "done_message")
    elif stage == "error":
        return t(ui_language, "error_message")
    else:
        return t(ui_language, "progress_idle")

    return t(ui_language, "progress_message").format(
        prefix=prefix,
    )


def estimate_progress_percent(processed_seconds, total_seconds):
    if not total_seconds or total_seconds <= 0:
        return None

    progress = float(processed_seconds / total_seconds) * 100.0
    return max(1.0, min(99.0, progress))


def create_progress_state(ui_language=DEFAULT_UI_LANGUAGE):
    now = time.time()
    return {
        "lock": threading.Lock(),
        "stage": "idle",
        "stage_updated_at": now,
        "started_at": now,
        "completed_at": None,
        "actual_percent": 0.0,
        "progress_updated_at": now,
        "display_percent": 0.0,
        "message": t(ui_language, "progress_idle"),
        "text": "",
        "download": None,
        "error_text": None,
        "done": False,
        "total_elapsed": None,
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
            if kwargs["done"] and state["completed_at"] is None:
                state["completed_at"] = now

        if "total_elapsed" in kwargs and kwargs["total_elapsed"] is not None:
            state["total_elapsed"] = float(kwargs["total_elapsed"])

        if "media_duration" in kwargs:
            state["media_duration"] = kwargs["media_duration"]

        if "has_actual_progress" in kwargs and kwargs["has_actual_progress"] is not None:
            state["has_actual_progress"] = kwargs["has_actual_progress"]


def get_progress_snapshot(state):
    with state["lock"]:
        return {
            "stage": state["stage"],
            "stage_updated_at": state["stage_updated_at"],
            "started_at": state["started_at"],
            "completed_at": state["completed_at"],
            "actual_percent": state["actual_percent"],
            "progress_updated_at": state["progress_updated_at"],
            "display_percent": state["display_percent"],
            "message": state["message"],
            "text": state["text"],
            "download": state["download"],
            "error_text": state["error_text"],
            "done": state["done"],
            "total_elapsed": state["total_elapsed"],
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


def run_transcription_task(temp_file_path, selected_language_label, selected_runtime_label, ui_language, state):
    ui_language = normalize_ui_language(ui_language)
    selected_language_label = normalize_transcription_language(selected_language_label)
    selected_runtime_label = normalize_runtime(selected_runtime_label)
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
            message=t(ui_language, "copying"),
        )

        shutil.copy(temp_file_path, local_file_path)
        print(f"\n📂 收到文件: {file_name} -> 正在处理...")

        media_duration = get_media_duration(local_file_path)
        if media_duration:
            initializing_message = t(ui_language, "duration_found").format(duration=media_duration)
        else:
            initializing_message = t(ui_language, "duration_unknown")

        update_progress_state(
            state,
            stage="initializing",
            actual_percent=8,
            message=t(ui_language, "preparing_runtime").format(message=initializing_message),
            media_duration=media_duration,
        )

        selected_model, runtime_profile = get_model_for_runtime(selected_runtime_label, ui_language)

        update_progress_state(
            state,
            stage="transcribing",
            actual_percent=12,
            message=t(ui_language, "model_started"),
        )

        selected_language_config = TRANSCRIPTION_LANGUAGE_OPTIONS.get(selected_language_label)
        selected_language = selected_language_config["code"] if selected_language_config else None
        transcribe_kwargs = {"beam_size": 5}
        if selected_language is not None:
            transcribe_kwargs["language"] = selected_language

        segments, info = selected_model.transcribe(local_file_path, **transcribe_kwargs)

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
                message=t(ui_language, "transcribing"),
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
            message=t(ui_language, "saving_result"),
            text=full_text,
        )

        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        duration = time.time() - start_time
        info_header = (
            t(ui_language, "done_header").format(
                duration=duration,
                runtime_label=get_runtime_label(selected_runtime_label, ui_language),
                device=runtime_profile["device"],
                compute_type=runtime_profile["compute_type"],
                language_label=get_transcription_language_label(selected_language_label, ui_language),
                detected_language=info.language,
            )
            + "=" * 30
            + "\n\n"
        )

        update_progress_state(
            state,
            stage="done",
            actual_percent=100,
            message=t(ui_language, "done_message"),
            text=info_header + full_text,
            download=txt_filename,
            total_elapsed=duration,
            done=True,
        )

    except Exception:
        error_text = f"❌ 运行报错:\n{traceback.format_exc()}"
        update_progress_state(
            state,
            stage="error",
            actual_percent=0,
            message=t(ui_language, "error_message"),
            error_text=error_text,
            done=True,
        )

    finally:
        if local_file_path and os.path.exists(local_file_path):
            try:
                os.remove(local_file_path)
            except:
                pass
def transcribe_audio(temp_file_path, selected_language_label, selected_runtime_label, ui_language):
    ui_language = normalize_ui_language(ui_language)
    selected_language_label = normalize_transcription_language(selected_language_label)
    selected_runtime_label = normalize_runtime(selected_runtime_label)

    # 检查是否为空 (如果用户清空了上传框)
    if temp_file_path is None:
        yield (
            render_progress_html(t(ui_language, "missing_file"), "idle", ui_language),
            t(ui_language, "missing_file"),
            gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label")),
        )
        return

    if not is_allowed_media_file(temp_file_path):
        message = t(ui_language, "invalid_file_body")
        yield render_progress_html(message, "error", ui_language), message, gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label"))
        return

    if selected_runtime_label not in DEVICE_PROFILES:
        message = t(ui_language, "missing_runtime")
        yield render_progress_html(message, "error", ui_language), message, gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label"))
        return

    state = create_progress_state(ui_language)
    worker = threading.Thread(
        target=run_transcription_task,
        args=(temp_file_path, selected_language_label, selected_runtime_label, ui_language, state),
        daemon=True,
    )
    worker.start()

    last_payload = None

    while True:
        snapshot = get_progress_snapshot(state)
        now = time.time()
        elapsed_seconds = (
            snapshot["total_elapsed"]
            if snapshot["total_elapsed"] is not None
            else now - snapshot["started_at"]
        )

        output_text = snapshot["error_text"] or snapshot["text"]
        status_text = snapshot["message"]
        if snapshot["stage"] not in {"done", "error", "idle"}:
            status_text = build_progress_message(
                snapshot["stage"],
                now,
                snapshot["has_actual_progress"],
                ui_language,
            )

        payload = (
            render_progress_html(
                status_text,
                get_progress_visual_state(snapshot["stage"]),
                ui_language,
                elapsed_seconds=elapsed_seconds,
                media_duration=snapshot["media_duration"],
                total_elapsed=snapshot["total_elapsed"],
            ),
            output_text,
            gr.update(
                value=snapshot["download"],
                visible=True,
                interactive=bool(snapshot["download"]),
                label=t(ui_language, "download_label"),
            ),
        )

        if payload != last_payload:
            yield payload
            last_payload = payload

        if snapshot["done"]:
            break

        time.sleep(0.2)


def render_invalid_file_notice(ui_language=DEFAULT_UI_LANGUAGE):
    ui_language = normalize_ui_language(ui_language)
    return f"""
    <div style="border:1px solid #fecaca;background:#fef2f2;color:#7f1d1d;border-radius:10px;padding:14px 16px;line-height:1.55;">
        <div style="font-weight:700;">{html.escape(t(ui_language, "invalid_file_body"))}</div>
    </div>
    """


def validate_media_upload(temp_file_path, ui_language):
    ui_language = normalize_ui_language(ui_language)
    if temp_file_path is None or is_allowed_media_file(temp_file_path):
        return (
            gr.update(value="", visible=False),
            gr.update(value=t(ui_language, "acknowledge"), visible=False),
            render_progress_html(t(ui_language, "progress_idle"), "idle", ui_language),
            "",
            gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label")),
        )

    return (
        gr.update(value=render_invalid_file_notice(ui_language), visible=True),
        gr.update(value=t(ui_language, "acknowledge"), visible=True),
        render_progress_html(t(ui_language, "invalid_file_body"), "error", ui_language),
        t(ui_language, "invalid_file_body"),
        gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label")),
    )


def build_ui_updates(ui_language, runtime_key, language_key, include_selector=False):
    ui_language = normalize_ui_language(ui_language)
    runtime_key = normalize_runtime(runtime_key)
    language_key = normalize_transcription_language(language_key)
    updates = [
        gr.update(value=t(ui_language, "app_title")),
        gr.update(value=t(ui_language, "intro")),
        gr.update(
            choices=get_runtime_choices(ui_language),
            value=get_runtime_component_value(runtime_key, ui_language),
            label=t(ui_language, "runtime_label"),
            info=t(ui_language, "runtime_info"),
        ),
        gr.update(value=render_runtime_status_html(runtime_key, ui_language)),
        gr.update(label=t(ui_language, "file_label")),
        gr.update(value=t(ui_language, "file_hint")),
        gr.update(
            choices=get_transcription_language_choices(ui_language),
            value=get_transcription_language_component_value(language_key, ui_language),
            label=t(ui_language, "language_label"),
            info=t(ui_language, "language_info"),
        ),
        gr.update(value=t(ui_language, "submit")),
        gr.update(value=render_progress_html(t(ui_language, "progress_idle"), "idle", ui_language)),
        gr.update(label=t(ui_language, "output_label")),
        gr.update(value=None, visible=True, interactive=False, label=t(ui_language, "download_label")),
        gr.update(value="", visible=False),
        gr.update(value=t(ui_language, "acknowledge"), visible=False),
        get_browser_preferences(ui_language, runtime_key, language_key),
    ]

    if include_selector:
        updates.insert(0, gr.update(value=ui_language))

    return updates


def restore_browser_preferences(preferences, request: gr.Request):
    preferences = preferences or DEFAULT_BROWSER_PREFS
    query_params = getattr(request, "query_params", {}) or {}
    ui_language = normalize_ui_language(query_params.get("ui", preferences.get("ui_language")))
    runtime_key = normalize_runtime(query_params.get("runtime", preferences.get("runtime")))
    language_key = normalize_transcription_language(
        query_params.get("lang", preferences.get("transcription_language"))
    )
    return build_ui_updates(ui_language, runtime_key, language_key, include_selector=True)


def apply_ui_language(ui_language, runtime_key, language_key):
    return build_ui_updates(ui_language, runtime_key, language_key, include_selector=False)


def update_runtime_selection(runtime_key, ui_language, language_key):
    ui_language = normalize_ui_language(ui_language)
    runtime_key = normalize_runtime(runtime_key)
    language_key = normalize_transcription_language(language_key)
    return (
        render_runtime_status_html(runtime_key, ui_language),
        get_browser_preferences(ui_language, runtime_key, language_key),
    )


def save_current_preferences(ui_language, runtime_key, language_key):
    return get_browser_preferences(ui_language, runtime_key, language_key)


# ============================================================
#                      界面 UI 定义
# ============================================================
CUSTOM_CSS = """
.top-language-picker { display:flex; justify-content:flex-end; align-items:flex-start; }
.top-language-picker .wrap { gap:6px; justify-content:flex-end; }
.top-language-picker label { margin-bottom:4px; }
"""

with gr.Blocks(title="Whisper 本地全能版") as demo:
    browser_preferences = gr.BrowserState(
        default_value=DEFAULT_BROWSER_PREFS,
        storage_key="whisper_project_ui_preferences_v2",
        secret="whisper_project_ui_preferences_secret",
    )

    with gr.Row():
        with gr.Column(scale=8):
            title_markdown = gr.Markdown(t(DEFAULT_UI_LANGUAGE, "app_title"))
            intro_markdown = gr.Markdown(t(DEFAULT_UI_LANGUAGE, "intro"))
        with gr.Column(scale=2, min_width=180, elem_classes=["top-language-picker"]):
            ui_language_selector = gr.Radio(
                label="ENG/中文",
                choices=UI_LANGUAGE_OPTIONS,
                value=DEFAULT_UI_LANGUAGE,
            )

    with gr.Row():
        with gr.Column(scale=1):
            runtime_selector = gr.Radio(
                label=t(DEFAULT_UI_LANGUAGE, "runtime_label"),
                choices=get_runtime_choices(DEFAULT_UI_LANGUAGE),
                value=None,
                info=t(DEFAULT_UI_LANGUAGE, "runtime_info"),
            )
            runtime_status = gr.HTML(render_runtime_status_html(None, DEFAULT_UI_LANGUAGE))

            # 1. 改用 File 组件，支持任意格式拖拽
            # 格式由 validate_media_upload 处理，方便给出可确认的错误提示并保留页面选择
            media_input = gr.File(
                label=t(DEFAULT_UI_LANGUAGE, "file_label"),
                type="filepath",
                height=100,
            )
            file_format_hint = gr.Markdown(t(DEFAULT_UI_LANGUAGE, "file_hint"))
            invalid_file_notice = gr.HTML(value="", visible=False)
            acknowledge_error_btn = gr.Button(
                t(DEFAULT_UI_LANGUAGE, "acknowledge"),
                variant="stop",
                visible=False,
            )

            language_selector = gr.Dropdown(
                label=t(DEFAULT_UI_LANGUAGE, "language_label"),
                choices=get_transcription_language_choices(DEFAULT_UI_LANGUAGE),
                value="auto",
                info=t(DEFAULT_UI_LANGUAGE, "language_info"),
            )

            submit_btn = gr.Button(t(DEFAULT_UI_LANGUAGE, "submit"), variant="primary")

        with gr.Column(scale=2):
            progress_display = gr.HTML(render_progress_html(t(DEFAULT_UI_LANGUAGE, "progress_idle"), "idle", DEFAULT_UI_LANGUAGE))
            output_text = gr.TextArea(label=t(DEFAULT_UI_LANGUAGE, "output_label"), lines=20)
            download_btn = gr.DownloadButton(
                label=t(DEFAULT_UI_LANGUAGE, "download_label"),
                value=None,
                variant="primary",
                size="lg",
                visible=True,
                interactive=False,
            )

    # ==================== 交互逻辑 ====================

    demo.load(
        fn=restore_browser_preferences,
        inputs=[browser_preferences],
        outputs=[
            ui_language_selector,
            title_markdown,
            intro_markdown,
            runtime_selector,
            runtime_status,
            media_input,
            file_format_hint,
            language_selector,
            submit_btn,
            progress_display,
            output_text,
            download_btn,
            invalid_file_notice,
            acknowledge_error_btn,
            browser_preferences,
        ],
        js="""
        (preferences) => {
            const params = new URLSearchParams(window.location.search);
            return [{
                ui_language: params.get("ui") || preferences?.ui_language || "中文",
                runtime: params.get("runtime") || preferences?.runtime || null,
                transcription_language: params.get("lang") || preferences?.transcription_language || "auto",
            }];
        }
        """,
    )

    ui_language_selector.change(
        fn=apply_ui_language,
        inputs=[ui_language_selector, runtime_selector, language_selector],
        outputs=[
            title_markdown,
            intro_markdown,
            runtime_selector,
            runtime_status,
            media_input,
            file_format_hint,
            language_selector,
            submit_btn,
            progress_display,
            output_text,
            download_btn,
            invalid_file_notice,
            acknowledge_error_btn,
            browser_preferences,
        ],
    )

    runtime_selector.change(
        fn=update_runtime_selection,
        inputs=[runtime_selector, ui_language_selector, language_selector],
        outputs=[runtime_status, browser_preferences],
    )

    language_selector.change(
        fn=save_current_preferences,
        inputs=[ui_language_selector, runtime_selector, language_selector],
        outputs=[browser_preferences],
    )

    media_input.change(
        fn=validate_media_upload,
        inputs=[media_input, ui_language_selector],
        outputs=[
            invalid_file_notice,
            acknowledge_error_btn,
            progress_display,
            output_text,
            download_btn,
        ],
    )

    acknowledge_error_btn.click(
        fn=None,
        inputs=[runtime_selector, language_selector, ui_language_selector],
        outputs=[],
        js="""
        (runtimeMode, speechLanguage, uiLanguage) => {
            const runtimeMap = {
                "cpu": "cpu",
                "gpu": "gpu",
                "CPU（兼容模式 / iGPU 电脑）": "cpu",
                "GPU（CUDA 加速 / dGPU 电脑）": "gpu",
                "CPU (Compatibility / iGPU)": "cpu",
                "GPU (CUDA acceleration / dGPU)": "gpu",
            };
            const languageMap = {
                "auto": "auto",
                "zh": "zh",
                "en": "en",
                "tl": "tl",
                "自动检测 / Auto Detect": "auto",
                "Auto Detect": "auto",
                "中文": "zh",
                "Chinese": "zh",
                "English": "en",
                "菲律宾语 / Filipino": "tl",
                "Filipino": "tl",
            };
            const params = new URLSearchParams();
            if (uiLanguage) params.set("ui", uiLanguage);
            if (runtimeMode) params.set("runtime", runtimeMap[runtimeMode] || runtimeMode);
            if (speechLanguage) params.set("lang", languageMap[speechLanguage] || speechLanguage);
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        }
        """,
    )

    # 只保留手动触发，避免“上传自动开始”与“按钮点击开始”重复执行同一任务
    submit_btn.click(
        fn=transcribe_audio,
        inputs=[media_input, language_selector, runtime_selector, ui_language_selector],
        outputs=[progress_display, output_text, download_btn]
    )

if __name__ == "__main__":
    # 启动网页
    demo.queue()
    demo.launch(inbrowser=True, css=CUSTOM_CSS)
