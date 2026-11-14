import os
import sys
import time
import json
import requests
import threading
import webbrowser
import torch

# Cấu hình cache HuggingFace linh hoạt giữa Windows, Linux và Docker
default_hf_home = r"D:\.cache\huggingface" if (os.name == 'nt' and os.path.exists(r"D:\.cache")) else os.path.expanduser("~/.cache/huggingface")
os.environ["HF_HOME"] = os.environ.get("HF_HOME", default_hf_home)

from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
from peft import PeftModel

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Paths & Config
chatbot_dir = os.path.dirname(os.path.abspath(__file__))
if chatbot_dir not in sys.path:
    sys.path.insert(0, chatbot_dir)

from rag_engine import CodebaseRAG, evaluate_architecture_compliance

root_dir = os.path.dirname(chatbot_dir)
lora_dir = os.path.join(root_dir, "outputs", "course-management-lora-adapter")
env_path = os.path.join(root_dir, ".env")
rag_engine = CodebaseRAG(root_dir)

# Nạp API Keys từ .env
gemini_api_key = ""
openai_api_key = ""
anthropic_api_key = ""
openrouter_api_key = ""
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                gemini_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("OPENAI_API_KEY="):
                openai_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("ANTHROPIC_API_KEY="):
                anthropic_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("OPENROUTER_API_KEY="):
                openrouter_api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

openrouter_api_key = os.environ.get("OPENROUTER_API_KEY", openrouter_api_key)

# Base model đọc từ adapter_config.json hoặc thư mục sharded
base_model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
default_sharded_path = r"D:\models\Qwen2.5-Coder-3B-Instruct-sharded" if (os.name == 'nt' and os.path.exists(r"D:\models")) else "/models/Qwen2.5-Coder-3B-Instruct-sharded"
sharded_model_path = os.environ.get("LOCAL_MODEL_PATH", default_sharded_path)
model_load_path = sharded_model_path if os.path.exists(sharded_model_path) else base_model_id

adapter_config_path = os.path.join(lora_dir, "adapter_config.json")
if os.path.exists(adapter_config_path):
    try:
        with open(adapter_config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            base_model_id = cfg.get("base_model_name_or_path", base_model_id)
    except Exception:
        pass

print("=" * 70)
print(f"KHỞI CHẠY HỆ THỐNG TRỢ LÝ AI NỘI BỘ (LOCAL GPU & SO SÁNH STREAMING)")
print(f"Base Model: {base_model_id} (Nguồn nạp: {model_load_path})")
print(f"LoRA Adapter: {lora_dir}")
print("=" * 70)

has_cuda = torch.cuda.is_available()
gpu_name = torch.cuda.get_device_name(0) if has_cuda else "CPU (Không có GPU)"
print(f"Thiết bị Local: {gpu_name}")
print(f"Cloud Gemini Key: {'Đã cấu hình' if gemini_api_key else 'Chưa có'}")
print(f"OpenRouter Key: {'Đã cấu hình (DeepSeek-V3 / Free Models)' if openrouter_api_key else 'Chưa có'}")

# Nạp Tokenizer
tokenizer = None
has_adapter = False
try:
    if os.path.exists(lora_dir):
        tokenizer = AutoTokenizer.from_pretrained(lora_dir)
        has_adapter = True
    else:
        tokenizer = AutoTokenizer.from_pretrained(base_model_id)
        has_adapter = False
    print("-> Đã nạp Tokenizer thành công!")
except Exception as e:
    print(f"[CẢNH BÁO]: Chưa thể nạp Tokenizer: {e}")

# Trạng thái nạp mô hình Local
local_ready = False
base_model = None
model = None

def init_local_model():
    global local_ready, base_model, model, has_adapter
    print(f"Đang nạp mô hình {base_model_id} lên GPU ({gpu_name})...")
    try:
        if has_cuda:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True
            )
            base_model = AutoModelForCausalLM.from_pretrained(
                model_load_path,
                quantization_config=bnb_config,
                device_map="auto"
            )
        else:
            base_model = AutoModelForCausalLM.from_pretrained(
                model_load_path,
                torch_dtype=torch.float32,
                device_map="cpu"
            )

        if os.path.exists(lora_dir):
            model = PeftModel.from_pretrained(base_model, lora_dir)
            has_adapter = True
        else:
            model = base_model
            has_adapter = False

        model.eval()
        local_ready = True
        allocated_mb = round(torch.cuda.memory_allocated(0)/(1024**2), 1) if has_cuda else 0
        print(f"-> [HOÀN TẤT 100% LOCAL]: Mô hình {base_model_id} + LoRA đã nạp xong vào GPU! (VRAM sử dụng: {allocated_mb} MB)\n")
    except Exception as e:
        print(f"[LỖI NẠP LOCAL GPU]: {e}")
        import traceback
        traceback.print_exc()

# Khởi chạy nạp mô hình trong luồng nền
threading.Thread(target=init_local_model, daemon=True).start()

# Prompts
SYSTEM_INSTRUCTION_PROJECT = (
    "Bạn là Kiến trúc sư Phần mềm Cao cấp chuyên gia Spring Boot 3 và Java 21 cho dự án Course Management System.\n"
    "Nhiệm vụ của bạn là viết mã nguồn Java tuân thủ 100% các chuẩn mực kiến trúc cốt lõi của dự án:\n"
    "1. Entity JPA: Sử dụng Jakarta Persistence (@Entity, @Table, @Id, @GeneratedValue, @Index, Lombok @Getter, @Setter, @Builder...).\n"
    "2. Tầng DAO: BẮT BUỘC phải kế thừa HibernatePaginationSortingDao<Pk, Entity> và implement interface IDao tương ứng.\n"
    "   - Constructor nhận EntityManager: super(Entity.class, entityManager);\n"
    "   - Gọi các phương thức dùng chung: super.create(), super.update(), deleteByPk(), get(), count(), findByHql().\n"
    "   - Bắt buộc áp dụng kiến trúc Hibernate Generic DAO tùy biến kế thừa HibernatePaginationSortingDao thay cho Spring Data JpaRepository.\n"
    "3. Tầng Service & Controller: Tách rõ Interface/Impl, sử dụng DTO Pattern (RequestDTO với Jakarta Validation, ResponseDTO).\n"
    "4. Quy chuẩn Package: Bắt buộc đặt trong package com.mkii.coursemanagementsystem (entity, dao, dao.impl, dto, service.impl, rest).\n"
    "5. Viết mã nguồn Java đầy đủ, chi tiết, kèm giải thích ngắn gọn, sẵn sàng copy vào dự án."
)

SYSTEM_INSTRUCTION_GENERAL = (
    "You are a general Java software engineer on the internet answering a user question.\n"
    "Write standard, conventional Spring Boot code using standard industry defaults: "
    "Spring Data JPA with standard JpaRepository interfaces (e.g. `public interface XRepository extends JpaRepository<X, Long>`), "
    "standard REST controllers, and standard general-purpose boilerplate without any custom enterprise architecture assumptions."
)

def retrieve_rag_for_query(user_message, top_k=3, max_chars=2600):
    """Truy xuất ngữ cảnh mã nguồn thật từ dự án để chống hallucination."""
    try:
        return rag_engine.format_context_block(user_message, top_k=top_k, max_chars=max_chars)
    except Exception:
        return "", []


def _normalize_history(history, max_turns=4, max_chars=550):
    """Chuẩn hóa lịch sử hội thoại nhiều lượt gọn nhẹ để giữ VRAM ổn định."""
    if not isinstance(history, list):
        return []
    cleaned = []
    for item in history[-(max_turns * 2):]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            cleaned.append({"role": role, "content": content[:max_chars]})
    return cleaned


def format_prompt(user_message, use_rag=True, rag_context=None, history=None):
    if use_rag:
        system_content = (
            SYSTEM_INSTRUCTION_PROJECT
            + "\n6. Bám sát tên class, field, package trong tài liệu tham khảo codebase bên dưới; không bịa tên class hoặc field không có."
        )
        if rag_context is None:
            rag_context, _ = retrieve_rag_for_query(user_message, top_k=3, max_chars=1800)
        final_user_content = (
            f"[YÊU CẦU]:\n{user_message}\n\n{rag_context}"
            if rag_context else user_message
        )
    else:
        # Base model không fine-tune, không RAG (đánh giá công bằng nguyên bản)
        system_content = (
            "You are a helpful Java and Spring Boot software engineering assistant. "
            "Answer the user's request cleanly and accurately in Vietnamese with complete Java code blocks."
        )
        final_user_content = user_message

    messages = [{"role": "system", "content": system_content}]
    if use_rag and history:
        messages.extend(_normalize_history(history))
    messages.append({"role": "user", "content": final_user_content})
    try:
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    except Exception:
        return f"<|im_start|>user\n{final_user_content}<|im_end|>\n<|im_start|>assistant\n"

# ======================================================================
# INFERENCE LOCAL GPU (ĐƯỢC TỐI ƯU HÓA VRAM & STREAMING)
# ======================================================================
def generate_local(user_message, use_adapter=True, max_tokens=1500, use_rag=None, rag_context=None):
    """Sinh câu trả lời 100% CỤC BỘ TRÊN GPU (RTX 4050)"""
    if use_rag is None:
        use_rag = bool(use_adapter)
    if not local_ready:
        for _ in range(20):
            if local_ready:
                break
            time.sleep(1)

    if not local_ready or model is None:
        return "⚠️ Mô hình Local đang được nạp vào VRAM GPU (khoảng 5-10 giây). Vui lòng thử lại sau giây lát!", 0.0

    formatted = format_prompt(user_message, use_rag=use_rag, rag_context=rag_context)
    inputs = tokenizer(formatted, return_tensors="pt")
    if has_cuda:
        inputs = inputs.to("cuda")

    start_time = time.time()
    is_code_req = any(w in user_message.lower() for w in [
        "viết", "tạo", "module", "entity", "dao", "dto", "hql", "sql", "class", 
        "code", "service", "triển khai", "hướng dẫn", "instructor", "enrollment", 
        "đăng ký", "thống kê", "specification", "bảo mật", "security", "xóa mềm", "audit"
    ])
    min_tokens = min(50, max_tokens) if is_code_req else min(5, max_tokens)
    with torch.inference_mode():
        if has_adapter and not use_adapter:
            with model.disable_adapter():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    min_new_tokens=min_tokens,
                    temperature=0.25,
                    top_p=0.9,
                    repetition_penalty=1.08,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
        else:
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                min_new_tokens=min_tokens,
                temperature=0.25,
                top_p=0.9,
                repetition_penalty=1.08,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
    elapsed = time.time() - start_time
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
    
    # Giải phóng VRAM rác sau mỗi phản hồi
    if has_cuda:
        torch.cuda.empty_cache()
        
    return response, round(elapsed, 2)

def generate_local_stream(user_message, use_adapter=True, max_tokens=1500, use_rag=None, rag_context=None, history=None):
    """Sinh câu trả lời STREAMING 100% CỤC BỘ TRÊN GPU (RTX 4050)"""
    if use_rag is None:
        use_rag = bool(use_adapter)
    if not local_ready or model is None:
        for _ in range(12):
            if local_ready and model is not None:
                break
            time.sleep(1)

    if not local_ready or model is None:
        yield "⚠️ Mô hình Local đang được nạp vào VRAM GPU... Vui lòng thử lại sau giây lát!"
        return

    formatted = format_prompt(user_message, use_rag=use_rag, rag_context=rag_context, history=history)
    inputs = tokenizer(formatted, return_tensors="pt")
    if has_cuda:
        inputs = inputs.to("cuda")

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    is_code_req = any(w in user_message.lower() for w in [
        "viết", "tạo", "module", "entity", "dao", "dto", "hql", "sql", "class", 
        "code", "service", "triển khai", "hướng dẫn", "instructor", "enrollment", 
        "đăng ký", "thống kê", "specification", "bảo mật", "security", "xóa mềm", "audit"
    ])
    min_tokens = min(50, max_tokens) if is_code_req else min(5, max_tokens)
    generation_kwargs = dict(
        **inputs,
        streamer=streamer,
        max_new_tokens=max_tokens,
        min_new_tokens=min_tokens,
        temperature=0.25,
        top_p=0.9,
        repetition_penalty=1.08,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    def run_generation():
        with torch.inference_mode():
            if has_adapter and not use_adapter:
                with model.disable_adapter():
                    model.generate(**generation_kwargs)
            else:
                model.generate(**generation_kwargs)

    thread = threading.Thread(target=run_generation)
    thread.start()

    for text_chunk in streamer:
        if text_chunk:
            yield text_chunk

    thread.join()
    if has_cuda:
        torch.cuda.empty_cache()

# ======================================================================
# CLOUD AI (GEMINI / CLAUDE ANTHROPIC) INFERENCE & STREAMING
# ======================================================================
CLOUD_MODELS = [
    'gemini-3-flash-preview',
    'gemini-3.5-flash',
    'gemini-flash-lite-latest',
    'gemini-2.5-flash',
    'gemini-flash-latest',
]
CLAUDE_MODELS = ['claude-3-7-sonnet-latest', 'claude-3-5-sonnet-latest', 'claude-sonnet-4-20250514']


def _extract_gemini_text(obj):
    """Trích xuất toàn bộ text non-thought từ mọi parts của phản hồi Gemini/Gemma."""
    chunks = []
    for cand in obj.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if part.get("thought"):
                continue
            txt = part.get("text")
            if txt:
                chunks.append(txt)
    return "".join(chunks)


def _format_cloud_error(status_code=None, detail=""):
    if status_code == 429:
        return "⚠️ Lỗi Cloud API (HTTP 429: Hết quota/rate-limit hiện tại). Vui lòng kiểm tra quota hoặc bổ sung API Key."
    if status_code == 401 or status_code == 403:
        return f"⚠️ Lỗi Cloud API (HTTP {status_code}: API Key không hợp lệ hoặc bị từ chối quyền)."
    if status_code:
        return f"⚠️ Lỗi Cloud API (HTTP {status_code}). {detail}".strip()
    return "⚠️ Không thể kết nối đến máy chủ Cloud AI. Vui lòng kiểm tra lại mạng hoặc API Key."


def _build_cloud_project_prompt(user_message, history=None):
    rag_block, _ = retrieve_rag_for_query(user_message, top_k=5, max_chars=5000)
    hist_items = _normalize_history(history, max_turns=4, max_chars=800)
    hist_block = ""
    if hist_items:
        lines = [f"- {'Người dùng' if m['role'] == 'user' else 'Trợ lý'}: {m['content']}" for m in hist_items]
        hist_block = "\n\n[LỊCH SỬ HỘI THOẠI GẦN ĐÂY]:\n" + "\n".join(lines)
    if rag_block:
        return f"{SYSTEM_INSTRUCTION_PROJECT}{hist_block}\n\n[YÊU CẦU CỦA NGƯỜI DÙNG]:\n{user_message}\n\n{rag_block}"
    return f"{SYSTEM_INSTRUCTION_PROJECT}{hist_block}\n\n[YÊU CẦU CỦA NGƯỜI DÙNG]:\n{user_message}"


def call_cloud_gemini(user_message, history=None):
    """Gọi Cloud AI (Gemini) với Ngữ cảnh Kiến trúc & RAG Codebase thật của dự án"""
    if not gemini_api_key:
        return "Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env", 0.0

    prompt = _build_cloud_project_prompt(user_message, history=history)
    start_time = time.time()
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 4096, 'temperature': 0.2}
    }

    last_status = None
    for m in CLOUD_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_api_key}"
        try:
            res = requests.post(url, json=payload, timeout=30)
            last_status = res.status_code
            if res.status_code == 200:
                text = _extract_gemini_text(res.json())
                if text:
                    elapsed = time.time() - start_time
                    return text, round(elapsed, 2)
        except Exception:
            continue

    elapsed = time.time() - start_time
    return _format_cloud_error(last_status), round(elapsed, 2)

def call_cloud_gemini_stream(user_message, history=None):
    """Streaming từ Cloud Gemini với ngữ cảnh kiến trúc + RAG codebase dự án"""
    if not gemini_api_key:
        yield "Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env"
        return

    prompt = _build_cloud_project_prompt(user_message, history=history)
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 4096, 'temperature': 0.2}
    }

    yielded_any = False
    for m in CLOUD_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:streamGenerateContent?alt=sse&key={gemini_api_key}"
        try:
            res = requests.post(url, json=payload, stream=True, timeout=35)
            if res.status_code == 200:
                for line in res.iter_lines():
                    if line:
                        line_str = line.decode('utf-8', errors='ignore')
                        if line_str.startswith('data:'):
                            try:
                                obj = json.loads(line_str[5:].strip())
                                text_part = _extract_gemini_text(obj)
                                if text_part:
                                    yielded_any = True
                                    yield text_part
                            except Exception:
                                pass
                if yielded_any:
                    return
        except Exception:
            continue

    if not yielded_any:
        # Fallback 1: OpenRouter DeepSeek V3 nếu có cấu hình
        if openrouter_api_key:
            prompt_or = _build_cloud_project_prompt(user_message, history=history)
            yielded_or = False
            for chunk in call_openrouter_stream(prompt_or, model="deepseek/deepseek-chat"):
                yielded_or = True
                yield chunk
            if yielded_or:
                return
        text, _ = call_cloud_gemini(user_message, history=history)
        yield text


def call_claude_stream(user_message, api_key="", system_prompt=SYSTEM_INSTRUCTION_GENERAL):
    """Streaming trực tiếp từ Anthropic Claude Messages API (Zero-Context nếu không nạp repo)."""
    key = (api_key or anthropic_api_key or "").strip()
    if not key:
        return

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    for m in CLAUDE_MODELS:
        payload = {
            "model": m,
            "max_tokens": 1800,
            "temperature": 0.2,
            "stream": True,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        try:
            res = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                stream=True,
                timeout=35,
            )
            if res.status_code == 200:
                for raw_line in res.iter_lines():
                    if not raw_line:
                        continue
                    line_str = raw_line.decode("utf-8", errors="ignore")
                    if line_str.startswith("data:"):
                        data_str = line_str[5:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            evt = json.loads(data_str)
                            if evt.get("type") == "content_block_delta":
                                delta = evt.get("delta", {})
                                if delta.get("type") == "text_delta" and delta.get("text"):
                                    yield delta["text"]
                        except Exception:
                            pass
                return
        except Exception:
            continue
    yield "⚠️ Không thể kết nối Anthropic Claude API với API Key đã cung cấp."


def call_openrouter_stream(user_message, system_prompt=None, model="deepseek/deepseek-chat", history=None):
    """Streaming từ OpenRouter API (mặc định DeepSeek-V3, fallback openrouter/free)."""
    key = (openrouter_api_key or os.environ.get("OPENROUTER_API_KEY") or "").strip()
    if not key:
        yield "⚠️ Chưa cấu hình OPENROUTER_API_KEY trong file .env."
        return

    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "Course Management Studio",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        for turn in _normalize_history(history):
            role = "user" if turn.get("role") == "user" else "assistant"
            content = turn.get("content", "").strip()
            if content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})

    models_to_try = [model] if model == "openrouter/free" else [model, "openrouter/free"]
    for m in models_to_try:
        payload = {
            "model": m,
            "messages": messages,
            "stream": True,
            "max_tokens": 4096,
            "temperature": 0.2
        }
        try:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                stream=True,
                timeout=35
            )
            if res.status_code == 200:
                yielded = False
                for raw_line in res.iter_lines():
                    if not raw_line:
                        continue
                    line_str = raw_line.decode("utf-8", errors="ignore")
                    if line_str.startswith("data:"):
                        chunk_str = line_str[5:].strip()
                        if chunk_str == "[DONE]":
                            break
                        try:
                            evt = json.loads(chunk_str)
                            choices = evt.get("choices", [])
                            if choices:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yielded = True
                                    yield content
                        except Exception:
                            pass
                if yielded:
                    return
        except Exception:
            continue
    yield "⚠️ Không thể kết nối OpenRouter API hoặc mô hình đang bận. Vui lòng thử lại sau."


def call_cloud_general_ai(user_message):
    """Mô phỏng AI tiêu chuẩn bên ngoài (Cloud AI - Zero Context Chưa Biết Dự Án)"""
    if not gemini_api_key:
        return "Lỗi: Chưa cấu hình API Key trong file .env", 0.0

    prompt = f"{SYSTEM_INSTRUCTION_GENERAL}\n\n[USER QUESTION]:\n{user_message}"
    start_time = time.time()
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 4096, 'temperature': 0.2}
    }

    last_status = None
    for m in CLOUD_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_api_key}"
        try:
            res = requests.post(url, json=payload, timeout=30)
            last_status = res.status_code
            if res.status_code == 200:
                text = _extract_gemini_text(res.json())
                if text:
                    elapsed = time.time() - start_time
                    return text, round(elapsed, 2)
        except Exception:
            continue

    elapsed = time.time() - start_time
    return _format_cloud_error(last_status), round(elapsed, 2)

def call_cloud_general_ai_stream(user_message, claude_key=""):
    """Streaming từ External Zero-Context AI (ưu tiên Claude API nếu có key, hoặc OpenRouter DeepSeek-V3, ngược lại dùng Gemini Zero-Context)"""
    effective_claude_key = (claude_key or anthropic_api_key or "").strip()
    if effective_claude_key:
        for chunk in call_claude_stream(user_message, api_key=effective_claude_key, system_prompt=SYSTEM_INSTRUCTION_GENERAL):
            yield chunk
        return

    # Nếu có OpenRouter API Key -> Dùng DeepSeek-V3 làm đối trọng chuẩn cực kỳ xuất sắc!
    if openrouter_api_key:
        yielded_or = False
        for chunk in call_openrouter_stream(user_message, system_prompt=SYSTEM_INSTRUCTION_GENERAL, model="deepseek/deepseek-chat"):
            yielded_or = True
            yield chunk
        if yielded_or:
            return

    if not gemini_api_key:
        yield "Lỗi: Chưa cấu hình API Key trong file .env"
        return

    prompt = f"{SYSTEM_INSTRUCTION_GENERAL}\n\n[USER QUESTION]:\n{user_message}"
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 4096, 'temperature': 0.2}
    }

    yielded_any = False
    for m in CLOUD_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:streamGenerateContent?alt=sse&key={gemini_api_key}"
        try:
            res = requests.post(url, json=payload, stream=True, timeout=30)
            if res.status_code == 200:
                for line in res.iter_lines():
                    if line:
                        line_str = line.decode('utf-8', errors='ignore')
                        if line_str.startswith('data:'):
                            try:
                                obj = json.loads(line_str[5:].strip())
                                text_part = _extract_gemini_text(obj)
                                if text_part:
                                    yielded_any = True
                                    yield text_part
                            except Exception:
                                pass
                if yielded_any:
                    return
        except Exception:
            continue

    if not yielded_any:
        ans, _ = call_cloud_general_ai(user_message)
        yield ans

def is_heavy_task(user_message):
    """Phân tích ý đồ: nếu là tạo cả dự án lớn nhiều file thì ủy quyền Cloud"""
    msg_lower = user_message.lower()
    heavy_keywords = [
        "tạo cho tôi 1 project", "tạo project mới", "project mới", "dự án mới", 
        "hệ thống mới", "viết toàn bộ", "toàn bộ hệ thống", "full project", 
        "kiến trúc tổng thể", "toàn bộ module", "cả dự án", "generate project",
        "create project", "tạo full source"
    ]
    return any(k in msg_lower for k in heavy_keywords)

# ======================================================================
# GIAO DIỆN WEB HIỆN ĐẠI (STREAMING, TOOLBAR, DIFF, CLIENT SESSIONS)
# ======================================================================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Management Studio - Bảng Điều Khiển Kỹ Thuật</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Marked.js for Markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Highlight.js for Code (Clean Light Theme) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        pre code { border-radius: 0.375rem; font-size: 0.815rem; line-height: 1.5; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
        .prose pre { padding: 0.85rem; background: #f8fafc; margin: 0.5rem 0; overflow-x: auto; border: 1px solid #e2e8f0; color: #1e293b; border-radius: 0.5rem; }
        .prose code { background: #f1f5f9; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.85em; color: #0f172a; font-weight: 500; }
        .prose p { margin-bottom: 0.65rem; color: #334155; line-height: 1.6; }
        .prose ul, .prose ol { margin-left: 1.25rem; margin-bottom: 0.65rem; list-style-type: disc; color: #334155; }
        .prose h1, .prose h2, .prose h3, .prose h4 { font-weight: 700; color: #0f172a; margin-top: 1rem; margin-bottom: 0.5rem; }
        .typing-cursor::after { content: '▋'; animation: blink 1s step-start infinite; color: #4f46e5; margin-left: 2px; }
        @keyframes blink { 50% { opacity: 0; } }
        .hidden { display: none !important; }
        .btn-mode-active {
            background-color: #eef2ff !important;
            color: #4338ca !important;
            border-left: 3px solid #4f46e5 !important;
            font-weight: 600 !important;
        }
        .btn-mode-inactive {
            color: #475569 !important;
            border-left: 3px solid transparent !important;
        }
        .btn-mode-inactive:hover {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        .quick-scroll::-webkit-scrollbar {
            height: 4px;
        }
        .quick-scroll::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 9999px;
        }
        .quick-scroll::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 9999px;
        }
        .quick-scroll::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        .quick-btn {
            cursor: pointer !important;
            user-select: none;
            transition: all 0.15s ease;
        }
        .quick-btn:hover {
            border-color: #6366f1 !important;
            background-color: #f5f3ff !important;
            color: #4338ca !important;
            transform: translateY(-1px);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex antialiased">

    <!-- Toast Notification -->
    <div id="toast-box" class="fixed top-5 right-5 z-50 pointer-events-none transition-all duration-300 opacity-0 transform -translate-y-2" style="display: none;">
        <div id="toast-msg" class="bg-slate-900 text-white text-xs font-medium px-4 py-2.5 rounded-lg shadow-lg flex items-center gap-2 border border-slate-800">
            <span>✓</span> <span>Đã chọn chế độ</span>
        </div>
    </div>

    <!-- ================================================================= -->
    <!-- TASKBAR / SIDEBAR CỐ ĐỊNH BÊN CẠNH (LEFT TASKBAR)                -->
    <!-- ================================================================= -->
    <aside class="w-72 bg-white border-r border-slate-200 flex flex-col h-screen flex-shrink-0 select-none shadow-[1px_0_4px_rgba(0,0,0,0.02)] z-20">
        
        <!-- Brand Header -->
        <div class="p-4 border-b border-slate-100 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-xs tracking-wider shadow-sm">
                    CMS
                </div>
                <div>
                    <h1 class="font-bold text-sm text-slate-900 leading-tight">Course Studio</h1>
                    <p class="text-[11px] text-slate-500 font-medium">Bảng Điều Khiển Kỹ Thuật</p>
                </div>
            </div>
        </div>

        <!-- Taskbar Menu Navigation -->
        <div class="p-3 overflow-y-auto flex-1 space-y-5">
            
            <!-- Nhóm 1: Chế Độ Xử Lý -->
            <div>
                <p class="px-2 text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Chế Độ Xử Lý</p>
                <div class="space-y-0.5">
                    <button type="button" onclick="setMode('hybrid')" id="btn-hybrid"
                            class="w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-active cursor-pointer">
                        <span class="text-sm">⚡</span>
                        <div class="flex-1 min-w-0">
                            <div class="font-semibold text-slate-900">Trợ Lý Kỹ Thuật (Hybrid)</div>
                            <div class="text-[10px] text-slate-500 truncate">Tự động Local & Cloud</div>
                        </div>
                    </button>
                    <button type="button" onclick="setMode('local')" id="btn-local"
                            class="w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-inactive cursor-pointer">
                        <span class="text-sm">💻</span>
                        <div class="flex-1 min-w-0">
                            <div class="font-semibold text-slate-800">100% Local GPU</div>
                            <div class="text-[10px] text-slate-500 truncate">RTX 4050 Offline</div>
                        </div>
                    </button>
                    <button type="button" onclick="setMode('cloud')" id="btn-cloud"
                            class="w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-inactive cursor-pointer">
                        <span class="text-sm">☁️</span>
                        <div class="flex-1 min-w-0">
                            <div class="font-semibold text-slate-800">Cloud Gemini (1M Context)</div>
                            <div class="text-[10px] text-slate-500 truncate">Sinh dự án quy mô lớn</div>
                        </div>
                    </button>
                    <button type="button" onclick="setMode('openrouter')" id="btn-openrouter"
                            class="w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-inactive cursor-pointer">
                        <span class="text-sm">🚀</span>
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center justify-between">
                                <div class="font-semibold text-slate-800">DeepSeek V3 (OpenRouter)</div>
                                <span class="text-[9px] px-1.5 py-0.2 rounded bg-purple-50 text-purple-700 font-semibold border border-purple-200">Cloud SOTA</span>
                            </div>
                            <div class="text-[10px] text-slate-500 truncate">DeepSeek-V3 + RAG Codebase</div>
                        </div>
                    </button>
                </div>
            </div>

            <!-- Nhóm 2: Lịch Sử Phiên Hỏi Đáp -->
            <div>
                <div class="px-2 flex items-center justify-between mb-1.5">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Lịch Sử Phiên</p>
                    <div class="flex items-center gap-1">
                        <button onclick="createNewSession()" title="Tạo phiên mới" class="text-[11px] text-indigo-600 hover:text-indigo-800 font-medium px-1.5 py-0.5 rounded hover:bg-indigo-50 transition cursor-pointer">
                            + Mới
                        </button>
                        <button onclick="clearAllHistory()" title="Xóa lịch sử" class="text-[11px] text-slate-400 hover:text-rose-600 px-1 py-0.5 rounded hover:bg-rose-50 transition cursor-pointer">
                            Xóa
                        </button>
                    </div>
                </div>
                <div id="history-list" class="space-y-1 text-xs max-h-56 overflow-y-auto pr-1">
                    <!-- Sessions rendered here -->
                </div>
            </div>

        </div>

        <!-- Sidebar Footer Status -->
        <div class="p-3 border-t border-slate-200 bg-slate-50/70 text-xs space-y-2">
            <div class="flex items-center justify-between text-[11px] text-slate-600">
                <span class="flex items-center gap-1.5 font-medium">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span>GPU RTX 4050 (Qwen-3B)</span>
                </span>
                <button type="button" onclick="refreshRagIndex()" id="rag-refresh-btn" title="Cập nhật chỉ mục mã nguồn RAG"
                        class="text-[10px] px-1.5 py-0.5 rounded bg-white border border-slate-200 hover:border-indigo-300 text-slate-600 hover:text-indigo-700 cursor-pointer">
                    ↻ RAG ({{ rag_count }})
                </button>
            </div>
            <div class="flex items-center gap-2 pt-1 border-t border-slate-200/80 text-[11px]">
                <a href="http://localhost:8080" target="_blank" class="text-indigo-600 hover:text-indigo-800 hover:underline flex items-center gap-1 font-medium">
                    <span>Web Quản Lý ↗</span>
                </a>
                <span class="text-slate-300">•</span>
                <a href="/benchmark-report" target="_blank" class="text-slate-600 hover:text-slate-900 hover:underline">
                    Báo Cáo Nghiệm Thu
                </a>
            </div>
        </div>

    </aside>

    <!-- ================================================================= -->
    <!-- KHÔNG GIAN LÀM VIỆC CHÍNH (MAIN WORKSPACE AREA)                   -->
    <!-- ================================================================= -->
    <main class="flex-1 flex flex-col h-screen overflow-hidden bg-slate-50/50">

        <!-- Top Header Navigation Bar -->
        <header class="h-14 border-b border-slate-200 bg-white px-6 flex items-center justify-between flex-shrink-0 z-10">
            <div class="flex items-center gap-2">
                <span id="header-mode-icon" class="text-base text-indigo-600 font-bold">⚡</span>
                <h2 id="header-mode-title" class="font-bold text-sm text-slate-900">Trợ Lý Kỹ Thuật (Hybrid)</h2>
                <span class="text-slate-300">|</span>
                <span class="text-xs text-slate-500 font-medium">Course Management System</span>
            </div>
            <div class="flex items-center gap-3 text-xs">
                <button type="button" onclick="clearChat()" class="px-2.5 py-1 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-md transition border border-slate-200 cursor-pointer">
                    Làm mới màn hình
                </button>
                <a href="http://localhost:8080/swagger-ui/index.html" target="_blank" class="px-2.5 py-1 text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 rounded-md transition border border-indigo-200 font-medium">
                    Swagger API Docs ↗
                </a>
            </div>
        </header>

        <!-- Sub-header: Mode Description & Quick Prompts -->
        <div class="px-6 pt-3 pb-1 border-b border-slate-200/60 bg-white/70">
            <!-- Mode Banner -->
            <div id="mode-banner" class="mb-2 bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-xs text-slate-600 flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="text-sm">💡</span>
                    <span id="mode-desc">Chế độ <strong>Trợ Lý Kỹ Thuật (Hybrid)</strong>: Local AI Qwen làm chủ, tự động điều phối Cloud AI khi cần sinh cả dự án lớn.</span>
                </div>
            </div>

            <!-- Quick Prompts Scrollbar -->
            <div class="flex items-center gap-2 overflow-x-auto pb-2 text-xs quick-scroll">
                <span class="text-slate-400 font-semibold whitespace-nowrap text-[11px] flex items-center gap-1">
                    Gợi ý:
                </span>
                <button type="button" onclick="fillPrompt('Viết mã nguồn Java đầy đủ gồm Entity Instructor và InstructorDaoImpl kế thừa HibernatePaginationSortingDao sử dụng EntityManager')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Module Giảng Viên
                </button>
                <button type="button" onclick="fillPrompt('Viết CourseDaoImpl tìm kiếm Khóa học nâng cao bằng Dynamic HQL và EntityManager kế thừa HibernatePaginationSortingDao')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Dynamic HQL DAO
                </button>
                <button type="button" onclick="fillPrompt('Viết CourseRequestDTO và CourseResponseDTO chuẩn Jakarta Validation (@NotBlank, @NotNull, @Min) và Lombok')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    DTO &amp; Validation
                </button>
                <button type="button" onclick="fillPrompt('Viết Document Entity lưu trữ file MinIO đa tầng tbl_document và DocumentDaoImpl kế thừa HibernatePaginationSortingDao')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Lưu trữ MinIO
                </button>
                <button type="button" onclick="fillPrompt('Viết Module Đăng ký Khóa học gồm Enrollment Entity liên kết Student-Course và EnrollmentDaoImpl kế thừa HibernatePaginationSortingDao')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Đăng Ký Khóa Học
                </button>
                <button type="button" onclick="fillPrompt('Viết GenericSpecification và GenericSpecificationsBuilder tìm kiếm Sinh viên theo tên, email, khoảng ngày sinh linh hoạt')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Lọc Đa Tiêu Chí
                </button>
                <button type="button" onclick="fillPrompt('Viết cấu hình phân quyền Spring Security và JWT, bảo vệ API với @PreAuthorize cho vai trò ADMIN')"
                        class="quick-btn bg-white hover:bg-indigo-50 text-slate-700 px-3 py-1 rounded-md border border-slate-200 transition whitespace-nowrap text-xs shadow-2xs">
                    Bảo Mật &amp; Phân Quyền
                </button>
                <button type="button" onclick="fillPrompt('Tạo cho tôi 1 project Quản lý Khách sạn gồm đầy đủ Entity, DAO, Service')"
                        class="quick-btn bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-3 py-1 rounded-md border border-indigo-200 transition whitespace-nowrap text-xs font-medium shadow-2xs">
                    Scaffold Dự Án Mới
                </button>
            </div>
        </div>

        <!-- Chat Output Scroll Box -->
        <div id="chat-box" class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            
            <!-- Welcome Card -->
            <div id="welcome-card" class="bg-white border border-slate-200 rounded-xl p-6 text-center max-w-2xl mx-auto my-auto shadow-sm">
                <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-lg mx-auto mb-3 border border-indigo-100">
                    CMS
                </div>
                <h3 class="text-base font-bold text-slate-900 mb-1.5">
                    Course Management Studio
                </h3>
                <p class="text-xs text-slate-500 mb-4 max-w-md mx-auto">
                    Môi trường lập trình chuyên biệt hỗ trợ sinh mã nguồn chuẩn Java 21, Spring Boot 3, Hibernate Generic DAO và đối chiếu đa mô hình.
                </p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-left">
                    <div class="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                        <span class="font-bold text-slate-900 flex items-center gap-1.5 mb-1">
                            💻 Xử Lý Cục Bộ Offline (RTX 4050)
                        </span>
                        <p class="text-slate-500 text-[11px] leading-relaxed">Chạy trực tiếp trên GPU máy trạm với Qwen-3B + LoRA. Bảo mật mã nguồn 100%.</p>
                    </div>
                    <div class="bg-slate-50 p-3.5 rounded-lg border border-slate-200">
                        <span class="font-bold text-slate-900 flex items-center gap-1.5 mb-1">
                            ⚖️ Đối Chiếu Đa Chiều Trực Quan
                        </span>
                        <p class="text-slate-500 text-[11px] leading-relaxed">So sánh trực tiếp chất lượng mã nguồn giữa Mô Hình Gốc, Mô Hình Fine-tuned và AI Tiêu Chuẩn.</p>
                    </div>
                </div>
            </div>

        </div>

        <!-- Sticky Bottom Input Box -->
        <div class="px-6 py-3 border-t border-slate-200 bg-white flex-shrink-0 relative">

            <!-- POPUP MENU CHỨC NĂNG (Action Hub Popup) -->
            <div id="action-menu-popup"
                 class="hidden absolute bottom-full mb-3 left-6 right-6 sm:right-auto sm:left-6 sm:w-[620px] bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col text-xs transition-all duration-150 animate-in fade-in"
                 style="max-height: 520px;">
                <!-- Header -->
                <div class="px-4 py-3 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="w-6 h-6 rounded-md bg-indigo-500/30 border border-indigo-400/30 flex items-center justify-center text-xs">⚡</span>
                        <div>
                            <h4 class="font-bold text-xs text-white flex items-center gap-1.5">
                                <span>Menu Chức Năng Hệ Thống</span>
                                <span class="text-[10px] font-normal text-indigo-300 bg-indigo-900/60 px-1.5 py-0.2 rounded border border-indigo-500/30">Course Studio Actions</span>
                            </h4>
                            <p class="text-[10px] text-slate-300">Chọn chế độ xử lý AI hoặc tiện ích hệ thống (Chế độ đối chiếu nằm ở nút [⚖️ Đối Chiếu])</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeActionMenu()" class="text-slate-400 hover:text-white p-1 rounded-md hover:bg-white/10 transition cursor-pointer" title="Đóng menu (ESC)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>
                </div>

                <!-- Search & Category Filter Bar -->
                <div class="p-3 bg-slate-50/80 border-b border-slate-200 space-y-2">
                    <div class="relative">
                        <input id="action-search-input" type="text"
                               placeholder="🔍 Tìm nhanh chế độ hoặc công cụ (gõ: hybrid, local, cloud, swagger, rag...)"
                               class="w-full text-xs pl-8 pr-3 py-2 bg-white border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 shadow-2xs"
                               oninput="handleActionSearch(event)"
                               onkeydown="handleActionMenuKey(event)">
                        <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    </div>

                    <!-- Category Tabs -->
                    <div class="flex items-center gap-1.5 overflow-x-auto text-[11px] quick-scroll pt-0.5">
                        <button type="button" onclick="filterActionCategory('all')" id="tab-cat-all" class="cat-tab px-2.5 py-1 rounded-md bg-indigo-600 text-white font-medium shadow-2xs cursor-pointer transition">
                            Tất cả (<span id="count-cat-all">0</span>)
                        </button>
                        <button type="button" onclick="filterActionCategory('modes')" id="tab-cat-modes" class="cat-tab px-2.5 py-1 rounded-md bg-white hover:bg-slate-100 text-slate-600 border border-slate-200 font-medium cursor-pointer transition">
                            ⚡ Chế Độ AI (<span id="count-cat-modes">0</span>)
                        </button>
                        <button type="button" onclick="filterActionCategory('tools')" id="tab-cat-tools" class="cat-tab px-2.5 py-1 rounded-md bg-white hover:bg-slate-100 text-slate-600 border border-slate-200 font-medium cursor-pointer transition">
                            🛠️ Công Cụ (<span id="count-cat-tools">0</span>)
                        </button>
                    </div>
                </div>

                <!-- Action Items List -->
                <div id="action-items-container" class="flex-1 overflow-y-auto p-2 space-y-1.5 max-h-[320px] bg-slate-50/40">
                    <!-- Action items rendered dynamically by JavaScript -->
                </div>

                <!-- Footer Tips -->
                <div class="px-3 py-2 bg-slate-50 border-t border-slate-200 text-[10px] text-slate-500 flex items-center justify-between">
                    <span class="flex items-center gap-1">
                        <span class="font-bold text-slate-700">Mẹo:</span>
                        <span>Click để chuyển chế độ hoặc mở công cụ • Gợi ý code đã ghim ở thanh trên cùng</span>
                    </span>
                    <span class="text-slate-400">Gõ <kbd class="px-1 py-0.5 bg-white border border-slate-200 rounded font-mono text-[9px]">ESC</kbd> để đóng</span>
                </div>
            </div>

            <!-- POPUP MENU ĐỐI CHIẾU & ĐÁNH GIÁ (Comparison Modes Popup) -->
            <div id="compare-menu-popup"
                 class="hidden absolute bottom-full mb-3 left-6 sm:left-24 w-full sm:w-[460px] max-w-[95vw] bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col text-xs transition-all duration-150 animate-in fade-in"
                 style="max-height: 480px;">
                <!-- Header -->
                <div class="px-4 py-3 bg-gradient-to-r from-amber-700 via-orange-800 to-amber-900 text-white flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="w-6 h-6 rounded-md bg-white/20 border border-white/20 flex items-center justify-center text-xs">⚖️</span>
                        <div>
                            <h4 class="font-bold text-xs text-white flex items-center gap-1.5">
                                <span>Đối Chiếu &amp; Đánh Giá Kiến Trúc</span>
                            </h4>
                            <p class="text-[10px] text-amber-100">Chọn chế độ so sánh chất lượng mã nguồn giữa các mô hình AI</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeCompareMenu()" class="text-amber-200 hover:text-white p-1 rounded-md hover:bg-white/10 transition cursor-pointer" title="Đóng menu (ESC)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>
                </div>

                <!-- 4 Options from the screenshot -->
                <div class="p-2 space-y-1.5 bg-slate-50/60 overflow-y-auto max-h-[360px]">
                    
                    <!-- Option 1: So Sánh Mô Hình -->
                    <div id="cmp-opt-compare_models" onclick="selectCompareMode('compare_models')"
                         class="cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 hover:bg-amber-50/60 transition cursor-pointer">
                        <div class="flex items-start gap-2.5 min-w-0 pr-2">
                            <span class="text-base p-1.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200/60 flex-shrink-0">⚖️</span>
                            <div class="min-w-0">
                                <div class="flex items-center gap-1.5 flex-wrap">
                                    <span class="font-bold text-slate-900 group-hover:text-amber-950 text-xs">So Sánh Mô Hình</span>
                                    <span class="text-[9px] px-1.5 py-0.2 rounded border bg-purple-50 text-purple-700 border-purple-200 font-medium">Offline GPU</span>
                                </div>
                                <div class="text-[11px] font-medium text-slate-600 mt-0.5">Base vs Fine-tuned GPU</div>
                                <p class="text-[10px] text-slate-400 mt-0.5">Chạy đối chiếu 2 mô hình cục bộ trên GPU RTX 4050 và tự động chấm điểm tuân thủ Generic DAO.</p>
                            </div>
                        </div>
                        <div class="cmp-check hidden text-emerald-600 font-bold text-xs flex-shrink-0 flex items-center gap-1 bg-emerald-50 px-2 py-1 rounded-md border border-emerald-200">
                            ✓ Đang chọn
                        </div>
                    </div>

                    <!-- Option 2: So Sánh Hệ Thống -->
                    <div id="cmp-opt-compare_system" onclick="selectCompareMode('compare_system')"
                         class="cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 hover:bg-amber-50/60 transition cursor-pointer">
                        <div class="flex items-start gap-2.5 min-w-0 pr-2">
                            <span class="text-base p-1.5 rounded-lg bg-blue-50 text-blue-700 border border-blue-200/60 flex-shrink-0">📋</span>
                            <div class="min-w-0">
                                <div class="flex items-center gap-1.5 flex-wrap">
                                    <span class="font-bold text-slate-900 group-hover:text-blue-950 text-xs">So Sánh Hệ Thống</span>
                                    <span class="text-[9px] px-1.5 py-0.2 rounded border bg-blue-50 text-blue-700 border-blue-200 font-medium">Hệ Thống vs Chuẩn</span>
                                </div>
                                <div class="text-[11px] font-medium text-slate-600 mt-0.5">Dự án vs AI Tiêu chuẩn</div>
                                <p class="text-[10px] text-slate-400 mt-0.5">Đối chiếu Hệ Thống Dự Án (LoRA + RAG) với AI Tiêu Chuẩn Bên Ngoài (Zero Context).</p>
                            </div>
                        </div>
                        <div class="cmp-check hidden text-emerald-600 font-bold text-xs flex-shrink-0 flex items-center gap-1 bg-emerald-50 px-2 py-1 rounded-md border border-emerald-200">
                            ✓ Đang chọn
                        </div>
                    </div>

                    <!-- Option 3: Đấu Trường 3 Chiều -->
                    <div id="cmp-opt-compare_arena" onclick="selectCompareMode('compare_arena')"
                         class="cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 hover:bg-amber-50/60 transition cursor-pointer">
                        <div class="flex items-start gap-2.5 min-w-0 pr-2">
                            <span class="text-base p-1.5 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200/60 flex-shrink-0">📊</span>
                            <div class="min-w-0">
                                <div class="flex items-center gap-1.5 flex-wrap">
                                    <span class="font-bold text-slate-900 group-hover:text-indigo-950 text-xs">Đấu Trường 3 Chiều</span>
                                    <span class="text-[9px] px-1.5 py-0.2 rounded border bg-indigo-50 text-indigo-700 border-indigo-200 font-medium">3 Luồng Song Song</span>
                                </div>
                                <div class="text-[11px] font-medium text-slate-600 mt-0.5">Đối chiếu 3 luồng song song</div>
                                <p class="text-[10px] text-slate-400 mt-0.5">3 luồng AI cùng sinh mã nguồn đồng thời: AI Tiêu Chuẩn, Base Model GPU và Fine-tuned LoRA+RAG GPU.</p>
                            </div>
                        </div>
                        <div class="cmp-check hidden text-emerald-600 font-bold text-xs flex-shrink-0 flex items-center gap-1 bg-emerald-50 px-2 py-1 rounded-md border border-emerald-200">
                            ✓ Đang chọn
                        </div>
                    </div>

                    <!-- Option 4: So Sánh Với Claude -->
                    <div id="cmp-opt-compare_claude" onclick="selectCompareMode('compare_claude')"
                         class="cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 hover:bg-amber-50/60 transition cursor-pointer">
                        <div class="flex items-start gap-2.5 min-w-0 pr-2">
                            <span class="text-base p-1.5 rounded-lg bg-orange-50 text-orange-700 border border-orange-200/60 flex-shrink-0">🤖</span>
                            <div class="min-w-0">
                                <div class="flex items-center gap-1.5 flex-wrap">
                                    <span class="font-bold text-slate-900 group-hover:text-orange-950 text-xs">So Sánh Với Claude</span>
                                    <span class="text-[9px] px-1.5 py-0.2 rounded border bg-orange-50 text-orange-700 border-orange-200 font-medium">API / Paste Test</span>
                                </div>
                                <div class="text-[11px] font-medium text-slate-600 mt-0.5">Chấm điểm kiến trúc trực tiếp</div>
                                <p class="text-[10px] text-slate-400 mt-0.5">Đối chiếu chất lượng với Claude (qua API hoặc paste kết quả) và chấm điểm tự động theo 5 tiêu chí.</p>
                            </div>
                        </div>
                        <div class="cmp-check hidden text-emerald-600 font-bold text-xs flex-shrink-0 flex items-center gap-1 bg-emerald-50 px-2 py-1 rounded-md border border-emerald-200">
                            ✓ Đang chọn
                        </div>
                    </div>

                </div>

                <!-- Footer -->
                <div class="px-3 py-2 bg-slate-50 border-t border-slate-200 text-[10px] text-slate-500 flex items-center justify-between">
                    <span>💡 Click để kích hoạt chế độ đối chiếu tương ứng</span>
                    <span class="text-slate-400">ESC để đóng</span>
                </div>
            </div>

            <!-- Chat Form with Action Button Inside -->
            <form id="chat-form" onsubmit="handleSend(event)" class="relative flex items-center">
                
                <!-- Cặp Nút Chức Năng & Đối Chiếu Nằm Trong Khung Chat -->
                <div class="absolute left-2.5 top-2.5 z-10 flex items-center gap-1.5">
                    <!-- Nút 1: Chức Năng (Tác vụ kiến trúc, prompt, công cụ) -->
                    <button type="button" id="btn-action-menu" onclick="toggleActionMenu(event)"
                            title="Bấm để mở danh sách chức năng (Phím tắt: /)"
                            class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 transition shadow-2xs text-xs font-semibold cursor-pointer select-none">
                        <span class="text-xs">⚡</span>
                        <span class="hidden sm:inline">Chức năng</span>
                        <svg id="action-menu-chevron" class="w-3.5 h-3.5 text-indigo-500 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </button>

                    <!-- Nút 2: Đối Chiếu & Đánh Giá (cạnh nút Chức Năng) -->
                    <button type="button" id="btn-compare-menu" onclick="toggleCompareMenu(event)"
                            title="Chọn chế độ Đối Chiếu & Đánh Giá (So sánh Mô hình, Hệ thống, Đấu trường, Claude)"
                            class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 transition shadow-2xs text-xs font-semibold cursor-pointer select-none">
                        <span id="compare-menu-icon" class="text-xs">⚖️</span>
                        <span id="compare-menu-label" class="inline">
                            <span class="hidden sm:inline lg:hidden">Đối Chiếu</span>
                            <span class="hidden lg:inline">Đối Chiếu &amp; Đánh Giá</span>
                        </span>
                        <svg id="compare-menu-chevron" class="w-3.5 h-3.5 text-amber-600 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>
                    </button>
                </div>

                <textarea id="user-input" rows="1" placeholder="Nhập câu hỏi hoặc yêu cầu tạo chức năng... (Shift+Enter để xuống dòng, gõ / để mở chức năng)"
                          class="w-full bg-slate-50 hover:bg-white focus:bg-white text-slate-800 placeholder-slate-400 rounded-xl pl-24 sm:pl-52 lg:pl-[290px] pr-24 py-3 border border-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-sm resize-none transition"
                          onkeydown="handleKeyDown(event)" oninput="handleInput(event)"></textarea>

                <button type="submit" id="send-btn"
                        class="absolute right-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition shadow-sm flex items-center gap-1.5 disabled:opacity-50 cursor-pointer">
                    <span>Gửi</span>
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                </button>
            </form>

            <div class="flex justify-between items-center text-[11px] text-slate-400 px-1 mt-1.5">
                <span>Nhấn <strong>Enter</strong> để gửi, <strong>Shift + Enter</strong> xuống dòng, gõ <strong>/</strong> để mở menu chức năng.</span>
                <span>Tự động tối ưu hóa kiến trúc</span>
            </div>
        </div>

    </main>

    <!-- ================================================================= -->
    <!-- JAVASCRIPT LOGIC PIPELINE                                         -->
    <!-- ================================================================= -->
    <script>
        let currentMode = 'hybrid';
        const defaultWelcomeHtml = document.getElementById('chat-box').innerHTML;

        const SERVER_HAS_CLAUDE_KEY = {{ 'true' if has_claude_key else 'false' }};
        const SERVER_HAS_OPENROUTER_KEY = {{ 'true' if has_openrouter_key else 'false' }};
        const modeDescriptions = {
            'hybrid': 'Chế độ <strong>Hybrid Auto</strong>: Tác vụ chuyên sâu chạy Local GPU + RAG Codebase; tác vụ kiến trúc lớn tự động chuyển Cloud 1M Context.',
            'local': 'Chế độ <strong>100% Local GPU</strong>: Chạy hoàn toàn Offline trên GPU RTX 4050 kết hợp QLoRA Adapter và truy xuất mã nguồn thật (RAG).',
            'openrouter': 'Chế độ <strong>DeepSeek V3 (Cloud OpenRouter)</strong>: Mô hình lập trình SOTA mã nguồn mở hàng đầu thế giới kết hợp ngữ cảnh RAG Codebase của dự án.',
            'cloud': 'Chế độ <strong>Google Gemini Cloud (1M Tokens Context)</strong>: Sử dụng Cloud Gemini với ngữ cảnh codebase thật của dự án.',
            'compare_models': 'Chế độ <strong>So Sánh Mô Hình (Gốc vs Fine-tuned + RAG)</strong>: Cả 2 mô hình chạy CỤC BỘ trên GPU RTX 4050 và chấm điểm kiến trúc tự động.',
            'compare_system': 'Chế độ <strong>So Sánh Hệ Thống</strong>: Đối chiếu Hệ Thống Dự Án (LoRA + RAG) với AI Tiêu Chuẩn Bên Ngoài (Zero Context).',
            'compare_arena': 'Chế độ <strong>Đấu Trường 3 Chiều</strong>: So sánh đồng thời 3 luồng (AI Tiêu Chuẩn Zero-Context, Base Model GPU, Fine-tuned + RAG GPU).',
            'compare_claude': 'Chế độ <strong>So Sánh Với Claude</strong>: Đối chiếu trực tiếp Dự Án (LoRA + RAG) với Claude (qua Anthropic API hoặc paste câu trả lời từ claude.ai để chấm điểm 5 tiêu chí kiến trúc).'
        };

        const modeTitles = {
            'hybrid': 'Trợ Lý Kỹ Thuật (Hybrid Auto)',
            'local': '100% Local GPU (Offline RTX 4050)',
            'openrouter': 'DeepSeek V3 (OpenRouter Cloud)',
            'cloud': 'Cloud Gemini (1M Context)',
            'compare_models': 'So Sánh Mô Hình (Gốc vs Fine-tuned)',
            'compare_system': 'So Sánh Hệ Thống (Dự Án vs AI Tiêu Chuẩn)',
            'compare_arena': 'Đấu Trường 3 Chiều',
            'compare_claude': 'So Sánh Trực Tiếp Với Claude'
        };

        const modeIcons = {
            'hybrid': '⚡',
            'local': '💻',
            'openrouter': '🚀',
            'cloud': '☁️',
            'compare_models': '⚖️',
            'compare_system': '📋',
            'compare_arena': '📊',
            'compare_claude': '🤖'
        };

        const modePlaceholders = {
            'hybrid': 'Nhập câu hỏi hoặc yêu cầu tạo chức năng... (Shift+Enter để xuống dòng)',
            'local': '[100% Local GPU] Nhập yêu cầu viết Entity, Generic DAO, HQL động...',
            'openrouter': '[DeepSeek V3] Nhập bài toán lập trình hoặc yêu cầu kỹ thuật...',
            'cloud': '[Cloud Gemini] Nhập yêu cầu thiết kế toàn bộ hệ thống lớn nhiều module...',
            'compare_models': '[So Sánh Mô Hình] Nhập bài toán để đối chiếu Model Gốc vs Fine-tuned + RAG...',
            'compare_system': '[So Sánh Hệ Thống] Nhập bài toán để so sánh Hệ Thống Dự Án vs AI Tiêu Chuẩn...',
            'compare_arena': '[Đấu Trường 3 Chiều] Nhập yêu cầu để 3 AI cùng sinh mã nguồn song song...',
            'compare_claude': '[Đối Chiếu Claude] Nhập câu hỏi về Course Management System để so tài với Claude...'
        };

        function showToast(msg, icon = "✓") {
            const box = document.getElementById('toast-box');
            const txt = document.getElementById('toast-msg');
            if (!box || !txt) return;
            txt.innerHTML = `<span>${icon}</span> <span>${msg}</span>`;
            box.style.display = 'block';
            setTimeout(() => {
                box.classList.remove('opacity-0', '-translate-y-2');
                box.classList.add('opacity-100', 'translate-y-0');
            }, 10);
            clearTimeout(window.__toastTimer);
            window.__toastTimer = setTimeout(() => {
                box.classList.remove('opacity-100', 'translate-y-0');
                box.classList.add('opacity-0', '-translate-y-2');
                setTimeout(() => { box.style.display = 'none'; }, 300);
            }, 2500);
        }

        function setMode(mode) {
            currentMode = mode;
            ['hybrid', 'local', 'openrouter', 'cloud', 'compare_models', 'compare_system', 'compare_arena', 'compare_claude'].forEach(m => {
                const btn = document.getElementById(`btn-${m}`);
                if (btn) {
                    if (m === mode) {
                        btn.className = "w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-active cursor-pointer";
                    } else {
                        btn.className = "w-full text-left px-3 py-2.5 rounded-lg text-xs transition flex items-center gap-2.5 btn-mode-inactive cursor-pointer";
                    }
                }
            });

            // Đồng bộ trạng thái nút & thẻ Đối Chiếu & Đánh Giá
            updateCompareMenuUI(mode);

            const headerTitle = document.getElementById('header-mode-title');
            if (headerTitle) headerTitle.textContent = modeTitles[mode] || mode;

            const headerIcon = document.getElementById('header-mode-icon');
            if (headerIcon) headerIcon.textContent = modeIcons[mode] || '⚡';

            const descEl = document.getElementById('mode-desc');
            if (descEl) descEl.innerHTML = modeDescriptions[mode] || '';

            const inputEl = document.getElementById('user-input');
            if (inputEl && modePlaceholders[mode]) {
                inputEl.placeholder = modePlaceholders[mode];
            }

            showToast(`Chế độ: ${modeTitles[mode] || mode}`, "✓");
        }

        const compareModesList = ['compare_models', 'compare_system', 'compare_arena', 'compare_claude'];
        const compareShortTitles = {
            'compare_models': 'So Sánh Model',
            'compare_system': 'So Sánh Hệ Thống',
            'compare_arena': 'Đấu Trường 3 Chiều',
            'compare_claude': 'So Sánh Claude'
        };

        function updateCompareMenuUI(mode) {
            const compareBtn = document.getElementById('btn-compare-menu');
            const compareIcon = document.getElementById('compare-menu-icon');
            const compareLabel = document.getElementById('compare-menu-label');
            if (compareBtn && compareIcon && compareLabel) {
                if (compareModesList.includes(mode)) {
                    compareBtn.className = "flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-100 hover:bg-amber-200 text-amber-900 border border-amber-300 ring-2 ring-amber-400/40 transition shadow-2xs text-xs font-bold cursor-pointer select-none";
                    compareIcon.textContent = modeIcons[mode] || '⚖️';
                    compareLabel.innerHTML = `<span>${compareShortTitles[mode] || modeTitles[mode]}</span>`;
                } else {
                    compareBtn.className = "flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 transition shadow-2xs text-xs font-semibold cursor-pointer select-none";
                    compareIcon.textContent = '⚖️';
                    compareLabel.innerHTML = `<span class="hidden sm:inline lg:hidden">Đối Chiếu</span><span class="hidden lg:inline">Đối Chiếu &amp; Đánh Giá</span>`;
                }
            }

            compareModesList.forEach(m => {
                const card = document.getElementById(`cmp-opt-${m}`);
                if (!card) return;
                const check = card.querySelector('.cmp-check');
                if (m === mode) {
                    card.className = "cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-amber-50/90 border border-amber-300 ring-1 ring-amber-400/40 shadow-xs transition cursor-pointer";
                    if (check) check.classList.remove('hidden');
                } else {
                    card.className = "cmp-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 hover:bg-amber-50/50 transition cursor-pointer";
                    if (check) check.classList.add('hidden');
                }
            });
        }

        function toggleCompareMenu(e) {
            if (e) e.stopPropagation();
            const popup = document.getElementById('compare-menu-popup');
            if (!popup) return;
            if (popup.classList.contains('hidden')) {
                closeActionMenu();
                openCompareMenu();
            } else {
                closeCompareMenu();
            }
        }

        function openCompareMenu() {
            const popup = document.getElementById('compare-menu-popup');
            const chevron = document.getElementById('compare-menu-chevron');
            const btn = document.getElementById('btn-compare-menu');
            if (!popup) return;

            popup.classList.remove('hidden');
            if (chevron) chevron.classList.add('rotate-180');
            if (btn) {
                btn.classList.add('bg-amber-100', 'border-amber-300', 'ring-2', 'ring-amber-400/40');
            }
            updateCompareMenuUI(currentMode);
        }

        function closeCompareMenu() {
            const popup = document.getElementById('compare-menu-popup');
            const chevron = document.getElementById('compare-menu-chevron');
            const btn = document.getElementById('btn-compare-menu');
            if (!popup) return;

            popup.classList.add('hidden');
            if (chevron) chevron.classList.remove('rotate-180');
            if (btn && !compareModesList.includes(currentMode)) {
                btn.classList.remove('bg-amber-100', 'border-amber-300', 'ring-2', 'ring-amber-400/40');
            }
        }

        function selectCompareMode(mode) {
            setMode(mode);
            closeCompareMenu();
            const el = document.getElementById('user-input');
            if (el) el.focus();
        }

        function handleKeyDown(e) {
            if (e.key === 'Escape') {
                closeActionMenu();
                closeCompareMenu();
                return;
            }
            if (e.key === '/' && (e.target.value === '' || e.target.value === '/')) {
                closeCompareMenu();
                setTimeout(() => openActionMenu(''), 10);
                return;
            }
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                closeActionMenu();
                closeCompareMenu();
                handleSend(e);
            }
        }

        function handleInput(e) {
            const val = e.target.value;
            if (val.startsWith('/')) {
                const query = val.slice(1).trim();
                const popup = document.getElementById('action-menu-popup');
                if (popup && popup.classList.contains('hidden')) {
                    openActionMenu(query);
                } else {
                    const searchInput = document.getElementById('action-search-input');
                    if (searchInput) {
                        searchInput.value = query;
                        filterActions(query, currentActionCategory);
                    }
                }
            }
        }

        function fillPrompt(text) {
            const el = document.getElementById('user-input');
            if (!el) return;
            el.value = text;
            el.focus();
            showToast(`Đã chọn gợi ý`, "✓");
            handleSend();
        }

        // ======================================================================
        // ACTION HUB / IN-CHAT FUNCTION MENU REGISTRY & HANDLERS
        // ======================================================================
        const CMS_ACTIONS = [
            // --- Chế Độ Xử Lý AI (Modes) ---
            {
                id: 'mode_hybrid',
                category: 'modes',
                categoryLabel: 'Chế Độ AI',
                title: 'Trợ Lý Kỹ Thuật (Hybrid Auto)',
                desc: 'Tự động phối hợp Local GPU RTX 4050 và Cloud 1M Tokens Context',
                mode: 'hybrid',
                icon: '⚡',
                badge: 'Chuyển Mode',
                badgeColor: 'bg-amber-50 text-amber-700 border-amber-200',
                keywords: 'hybrid auto tro ly ky thuat local cloud che do mode'
            },
            {
                id: 'mode_local',
                category: 'modes',
                categoryLabel: 'Chế Độ AI',
                title: '100% Local GPU (Offline RTX 4050)',
                desc: 'Chạy hoàn toàn trên GPU cục bộ với Qwen-3B + LoRA Adapter và RAG Codebase',
                mode: 'local',
                icon: '💻',
                badge: 'Chuyển Mode',
                badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
                keywords: 'local gpu offline rtx 4050 qwen lora qlora che do mode'
            },
            {
                id: 'mode_cloud',
                category: 'modes',
                categoryLabel: 'Chế Độ AI',
                title: 'Cloud Gemini (1M Context)',
                desc: 'Sinh kiến trúc quy mô lớn với context sâu 1 triệu tokens',
                mode: 'cloud',
                icon: '☁️',
                badge: 'Chuyển Mode',
                badgeColor: 'bg-sky-50 text-sky-700 border-sky-200',
                keywords: 'cloud gemini 1m context token quy mo lon che do mode'
            },
            {
                id: 'mode_openrouter',
                category: 'modes',
                categoryLabel: 'Chế Độ AI',
                title: 'DeepSeek V3 (Cloud OpenRouter)',
                desc: 'Mô hình coding SOTA mã nguồn mở qua OpenRouter API + RAG Codebase',
                mode: 'openrouter',
                icon: '🚀',
                badge: 'Chuyển Mode',
                badgeColor: 'bg-purple-50 text-purple-700 border-purple-200',
                keywords: 'deepseek v3 openrouter cloud coding rag sota che do mode'
            },

            // --- Công Cụ & Báo Cáo ---
            {
                id: 'tool_benchmark_report',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Mở Báo Cáo Nghiệm Thu Trực Quan',
                desc: 'Xem báo cáo HTML trực quan với biểu đồ đánh giá đối chiếu hiệu năng mô hình',
                toolFn: () => window.open('/benchmark-report', '_blank'),
                icon: '📈',
                badge: 'Mở Báo Cáo',
                badgeColor: 'bg-indigo-50 text-indigo-700 border-indigo-200',
                keywords: 'bao cao nghiem thu truc quan html chart benchmark so sanh'
            },
            {
                id: 'tool_swagger',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Swagger API Documentation',
                desc: 'Tài liệu OpenAPI và giao diện tương tác REST API Spring Boot (cổng 8080)',
                toolFn: () => window.open('http://localhost:8080/swagger-ui/index.html', '_blank'),
                icon: '📜',
                badge: 'Swagger :8080',
                badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
                keywords: 'swagger api docs rest openapi endpoints backend 8080'
            },
            {
                id: 'tool_web_manager',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Web Quản Lý CMS',
                desc: 'Mở giao diện quản lý khóa học, sinh viên, dashboard thống kê (cổng 8080)',
                toolFn: () => window.open('http://localhost:8080', '_blank'),
                icon: '🌐',
                badge: 'Web App :8080',
                badgeColor: 'bg-blue-50 text-blue-700 border-blue-200',
                keywords: 'web quan ly cms admin dashboard course student 8080'
            },
            {
                id: 'tool_refresh_rag',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Cập Nhật Chỉ Mục RAG Codebase',
                desc: 'Quét lại toàn bộ file mã nguồn Java, Config, DTO của dự án vào bộ nhớ RAG',
                toolFn: () => refreshRagIndex(),
                icon: '↻',
                badge: 'Quét RAG',
                badgeColor: 'bg-sky-50 text-sky-700 border-sky-200',
                keywords: 'cap nhat rag index scan quet lai codebase vector'
            },
            {
                id: 'tool_new_session',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Tạo Phiên Làm Việc Mới',
                desc: 'Lưu phiên làm việc hiện tại và bắt đầu phiên hỏi đáp mới sạch sẽ',
                toolFn: () => createNewSession(),
                icon: '📝',
                badge: 'Phiên Mới',
                badgeColor: 'bg-slate-100 text-slate-700 border-slate-200',
                keywords: 'tao phien moi new session clear reset'
            },
            {
                id: 'tool_clear_screen',
                category: 'tools',
                categoryLabel: 'Công Cụ & Báo Cáo',
                title: 'Làm Mới Màn Hình Chat',
                desc: 'Xóa sạch các tin nhắn đang hiển thị trên màn hình chat hiện tại',
                toolFn: () => clearChat(),
                icon: '🧹',
                badge: 'Xóa Màn Hình',
                badgeColor: 'bg-rose-50 text-rose-700 border-rose-200',
                keywords: 'lam moi man hinh clear chat xoa man hinh'
            }
        ];

        let currentActionCategory = 'all';

        function toggleActionMenu(e) {
            if (e) e.stopPropagation();
            const popup = document.getElementById('action-menu-popup');
            if (popup.classList.contains('hidden')) {
                openActionMenu();
            } else {
                closeActionMenu();
            }
        }

        function openActionMenu(initialQuery = '') {
            closeCompareMenu();
            const popup = document.getElementById('action-menu-popup');
            const chevron = document.getElementById('action-menu-chevron');
            const btn = document.getElementById('btn-action-menu');
            if (!popup) return;

            popup.classList.remove('hidden');
            if (chevron) chevron.classList.add('rotate-180');
            if (btn) {
                btn.classList.add('bg-indigo-100', 'text-indigo-800', 'border-indigo-300');
            }

            const searchInput = document.getElementById('action-search-input');
            if (searchInput) {
                searchInput.value = initialQuery;
                setTimeout(() => searchInput.focus(), 50);
            }
            filterActions(initialQuery, currentActionCategory);
        }

        function closeActionMenu() {
            const popup = document.getElementById('action-menu-popup');
            const chevron = document.getElementById('action-menu-chevron');
            const btn = document.getElementById('btn-action-menu');
            if (!popup) return;

            popup.classList.add('hidden');
            if (chevron) chevron.classList.remove('rotate-180');
            if (btn) {
                btn.classList.remove('bg-indigo-100', 'text-indigo-800', 'border-indigo-300');
            }

            const inputEl = document.getElementById('user-input');
            if (inputEl && inputEl.value === '/') {
                inputEl.value = '';
            }
        }

        function filterActionCategory(cat) {
            currentActionCategory = cat;
            ['all', 'modes', 'tools'].forEach(c => {
                const tab = document.getElementById(`tab-cat-${c}`);
                if (!tab) return;
                if (c === cat) {
                    tab.className = "cat-tab px-2.5 py-1 rounded-md bg-indigo-600 text-white font-medium shadow-2xs cursor-pointer transition";
                } else {
                    tab.className = "cat-tab px-2.5 py-1 rounded-md bg-white hover:bg-slate-100 text-slate-600 border border-slate-200 font-medium cursor-pointer transition";
                }
            });

            const searchInput = document.getElementById('action-search-input');
            const query = searchInput ? searchInput.value.trim() : '';
            filterActions(query, cat);
        }

        function handleActionSearch(e) {
            const query = e.target.value.trim();
            filterActions(query, currentActionCategory);
        }

        function filterActions(query, category) {
            const q = query.toLowerCase();
            const filtered = CMS_ACTIONS.filter(item => {
                const matchCat = (category === 'all' || item.category === category);
                if (!matchCat) return false;
                if (!q) return true;
                return item.title.toLowerCase().includes(q) ||
                       item.desc.toLowerCase().includes(q) ||
                       item.badge.toLowerCase().includes(q) ||
                       item.keywords.toLowerCase().includes(q);
            });

            // Update badge counts
            const countAll = CMS_ACTIONS.filter(i => !q || i.title.toLowerCase().includes(q) || i.desc.toLowerCase().includes(q) || i.keywords.toLowerCase().includes(q)).length;
            const countModes = CMS_ACTIONS.filter(i => i.category === 'modes' && (!q || i.title.toLowerCase().includes(q) || i.desc.toLowerCase().includes(q) || i.keywords.toLowerCase().includes(q))).length;
            const countTools = CMS_ACTIONS.filter(i => i.category === 'tools' && (!q || i.title.toLowerCase().includes(q) || i.desc.toLowerCase().includes(q) || i.keywords.toLowerCase().includes(q))).length;

            const elAll = document.getElementById('count-cat-all');
            const elModes = document.getElementById('count-cat-modes');
            const elTools = document.getElementById('count-cat-tools');
            if (elAll) elAll.textContent = countAll;
            if (elModes) elModes.textContent = countModes;
            if (elTools) elTools.textContent = countTools;

            renderActionList(filtered);
        }

        function renderActionList(items) {
            const container = document.getElementById('action-items-container');
            if (!container) return;

            if (items.length === 0) {
                container.innerHTML = `
                    <div class="p-6 text-center text-slate-400 text-xs">
                        <span class="text-2xl block mb-1">🔍</span>
                        <p class="font-semibold text-slate-600">Không tìm thấy chức năng phù hợp</p>
                        <p class="text-[11px] text-slate-400 mt-0.5">Thử tìm với: <code>claude</code>, <code>gpu</code>, <code>arena</code>, <code>swagger</code>, <code>rag</code>, <code>phiên mới</code></p>
                    </div>
                `;
                return;
            }

            container.innerHTML = items.map((item, idx) => {
                const isCode = item.category === 'code';
                const isMode = item.category === 'modes';
                const isTool = item.category === 'tools';

                let rightActionsHtml = '';
                if (isCode) {
                    rightActionsHtml = `
                        <div class="flex items-center gap-1 flex-shrink-0" onclick="event.stopPropagation()">
                            <button type="button" title="Chèn vào ô chat để chỉnh sửa trước khi gửi"
                                    onclick="insertActionPrompt('${item.id}')"
                                    class="text-[10px] px-2 py-1 bg-white hover:bg-slate-100 text-slate-600 rounded-md border border-slate-200 hover:border-slate-300 font-medium transition cursor-pointer">
                                ✏️ Chèn
                            </button>
                            <button type="button" title="Gửi ngay câu lệnh này"
                                    onclick="executeAction('${item.id}')"
                                    class="text-[10px] px-2.5 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md font-semibold transition shadow-2xs flex items-center gap-1 cursor-pointer">
                                <span>Gửi</span>
                                <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                            </button>
                        </div>
                    `;
                } else if (isMode) {
                    rightActionsHtml = `
                        <button type="button" onclick="executeAction('${item.id}')"
                                class="text-[10px] px-2.5 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-md font-semibold transition shadow-2xs flex items-center gap-1 cursor-pointer flex-shrink-0">
                            <span>Chuyển</span>
                            <span class="text-xs">→</span>
                        </button>
                    `;
                } else {
                    rightActionsHtml = `
                        <button type="button" onclick="executeAction('${item.id}')"
                                class="text-[10px] px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 rounded-md font-semibold transition shadow-2xs flex items-center gap-1 cursor-pointer flex-shrink-0">
                            <span>Mở</span>
                            <span class="text-xs">↗</span>
                        </button>
                    `;
                }

                return `
                    <div class="action-card group flex items-center justify-between p-2.5 rounded-xl bg-white border border-slate-200/90 hover:border-indigo-300 hover:bg-indigo-50/50 hover:shadow-xs transition cursor-pointer"
                         onclick="executeAction('${item.id}')" data-id="${item.id}" data-index="${idx}">
                        <div class="flex items-start gap-2.5 min-w-0 pr-2">
                            <span class="text-base p-1.5 rounded-lg bg-slate-100 group-hover:bg-white border border-slate-200/80 flex-shrink-0">
                                ${item.icon}
                            </span>
                            <div class="min-w-0">
                                <div class="flex items-center gap-1.5 flex-wrap">
                                    <span class="font-bold text-slate-900 group-hover:text-indigo-950 text-xs">${item.title}</span>
                                    <span class="text-[9px] px-1.5 py-0.2 rounded border ${item.badgeColor} font-medium">${item.badge}</span>
                                </div>
                                <p class="text-[11px] text-slate-500 line-clamp-1 mt-0.5">${item.desc}</p>
                            </div>
                        </div>
                        ${rightActionsHtml}
                    </div>
                `;
            }).join('');
        }

        function executeAction(id) {
            const item = CMS_ACTIONS.find(a => a.id === id);
            if (!item) return;

            if (item.category === 'code') {
                closeActionMenu();
                fillPrompt(item.prompt);
            } else if (item.category === 'modes') {
                closeActionMenu();
                setMode(item.mode);
                const el = document.getElementById('user-input');
                if (el) el.focus();
            } else if (item.category === 'tools') {
                closeActionMenu();
                if (typeof item.toolFn === 'function') {
                    item.toolFn();
                }
            }
        }

        function insertActionPrompt(id) {
            const item = CMS_ACTIONS.find(a => a.id === id);
            if (!item || !item.prompt) return;

            const el = document.getElementById('user-input');
            if (!el) return;
            el.value = item.prompt;
            closeActionMenu();
            el.focus();
            el.setSelectionRange(item.prompt.length, item.prompt.length);
            showToast(`Đã chèn câu lệnh vào ô chat để chỉnh sửa`, "✏️");
        }

        function handleActionMenuKey(e) {
            if (e.key === 'Escape') {
                e.preventDefault();
                closeActionMenu();
                const el = document.getElementById('user-input');
                if (el) el.focus();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                const firstCard = document.querySelector('.action-card');
                if (firstCard) {
                    const id = firstCard.getAttribute('data-id');
                    executeAction(id);
                }
            }
        }

        let chatHistory = [];

        function clearChat() {
            chatHistory = [];
            document.getElementById('chat-box').innerHTML = defaultWelcomeHtml;
        }

        async function refreshRagIndex() {
            const btn = document.getElementById('rag-refresh-btn');
            if (btn) btn.textContent = '↻ Đang quét...';
            try {
                const res = await fetch('/api/rag/refresh', { method: 'POST' });
                const data = await res.json();
                if (btn) btn.textContent = `↻ RAG (${data.indexed_files || 0})`;
                showToast(`Đã làm mới RAG: ${data.indexed_files || 0} chỉ mục`, "✓");
            } catch (e) {
                if (btn) btn.textContent = '↻ RAG lỗi';
                showToast("Không thể làm mới RAG", "⚠️");
            }
        }

        // ======================================================================
        // CLIENT-SIDE CHAT HISTORY (localStorage)
        // ======================================================================
        function getSessions() {
            try {
                return JSON.parse(localStorage.getItem('cms_ai_sessions') || localStorage.getItem('cms_copilot_sessions') || '[]');
            } catch (e) {
                return [];
            }
        }

        function saveSession(promptText, mode, htmlContent) {
            const sessions = getSessions();
            const id = 'sess_' + Date.now();
            const now = new Date();
            const timeStr = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }) + ' ' + now.toLocaleDateString('vi-VN');
            sessions.unshift({
                id: id,
                prompt: promptText,
                mode: mode,
                time: timeStr,
                html: htmlContent
            });
            if (sessions.length > 30) sessions.pop();
            localStorage.setItem('cms_ai_sessions', JSON.stringify(sessions));
            renderHistorySidebar();
        }

        function renderHistorySidebar() {
            const list = document.getElementById('history-list');
            if (!list) return;
            const sessions = getSessions();
            if (sessions.length === 0) {
                list.innerHTML = '<div class="text-slate-400 text-center py-4 text-[11px]">Chưa có phiên lưu trữ.</div>';
                return;
            }
            list.innerHTML = sessions.map(s => `
                <div onclick="restoreSession('${s.id}')" class="p-2 rounded-lg bg-slate-50 hover:bg-indigo-50/60 border border-slate-200/80 hover:border-indigo-200 cursor-pointer transition group">
                    <div class="flex items-center justify-between text-[10px] text-slate-400 mb-0.5">
                        <span class="px-1.5 py-0.2 rounded bg-slate-200 text-slate-600 font-mono">${escapeHtml(s.mode)}</span>
                        <span>${escapeHtml(s.time.split(' ')[0])}</span>
                    </div>
                    <div class="text-[11px] text-slate-700 line-clamp-1 font-medium group-hover:text-indigo-900">
                        ${escapeHtml(s.prompt)}
                    </div>
                </div>
            `).join('');
        }

        function restoreSession(id) {
            const sessions = getSessions();
            const sess = sessions.find(s => s.id === id);
            if (!sess) return;
            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = sess.html;
            enhanceCodeBlocks(chatBox);
            showToast("Đã khôi phục phiên hỏi đáp", "✓");
        }

        function clearAllHistory() {
            if (confirm('Bạn có chắc muốn xóa toàn bộ lịch sử hỏi đáp?')) {
                localStorage.removeItem('cms_ai_sessions');
                localStorage.removeItem('cms_copilot_sessions');
                renderHistorySidebar();
                showToast("Đã xóa toàn bộ lịch sử", "✓");
            }
        }

        function createNewSession() {
            clearChat();
            showToast("Đã tạo phiên hỏi đáp mới", "✓");
        }

        // ======================================================================
        // CODE TOOLBAR & ARCHITECTURAL HIGHLIGHTER
        // ======================================================================
        function enhanceCodeBlocks(container) {
            if (!container) container = document;
            container.querySelectorAll('pre code').forEach((block) => {
                if (block.closest('.code-toolbar-wrapper')) return;

                hljs.highlightElement(block);

                const pre = block.parentElement;
                const codeText = block.innerText;

                let lang = 'Java';
                block.classList.forEach(cls => {
                    if (cls.startsWith('language-')) lang = cls.replace('language-', '').toUpperCase();
                });

                // Kiểm tra kiến trúc
                let archBadge = '';
                const hasJpaRepo = /JpaRepository|CrudRepository/i.test(codeText);
                const hasGenericDao = /HibernatePaginationSortingDao|IPaginationSortingDao/i.test(codeText);

                if (hasJpaRepo && !hasGenericDao) {
                    archBadge = `
                        <div class="px-3 py-1.5 bg-rose-50 border-b border-rose-200 text-[11px] text-rose-800 flex items-center justify-between">
                            <span class="flex items-center gap-1.5 font-medium">
                                <span>⚠️</span> <span><strong>Cảnh báo:</strong> Sử dụng <code>JpaRepository</code> (Không kế thừa Generic DAO chuẩn)</span>
                            </span>
                            <span class="text-rose-600 font-mono text-[10px] font-semibold">Sai chuẩn</span>
                        </div>
                    `;
                } else if (hasGenericDao) {
                    archBadge = `
                        <div class="px-3 py-1.5 bg-emerald-50 border-b border-emerald-200 text-[11px] text-emerald-800 flex items-center justify-between">
                            <span class="flex items-center gap-1.5 font-medium">
                                <span>✓</span> <span><strong>Chuẩn Kiến Trúc:</strong> Kế thừa <code>HibernatePaginationSortingDao</code> &amp; <code>EntityManager</code></span>
                            </span>
                            <span class="text-emerald-700 font-mono text-[10px] font-semibold">Tương thích 100%</span>
                        </div>
                    `;
                }

                // Bọc Toolbar
                const wrapper = document.createElement('div');
                wrapper.className = 'code-toolbar-wrapper my-3 rounded-lg border border-slate-200 bg-white overflow-hidden shadow-2xs';

                const header = document.createElement('div');
                header.className = 'flex items-center justify-between px-3 py-1.5 bg-slate-50 border-b border-slate-200 text-xs text-slate-600';
                header.innerHTML = `
                    <span class="font-mono text-[11px] text-slate-700 font-semibold flex items-center gap-1.5">
                        <span>☕</span> ${lang}
                    </span>
                    <div class="flex items-center gap-2">
                        <button onclick="copyCodeSnippet(this)" class="px-2 py-0.5 rounded bg-white hover:bg-slate-100 text-slate-700 text-[11px] transition flex items-center gap-1 border border-slate-200 cursor-pointer shadow-2xs">
                            Sao chép
                        </button>
                        <button onclick="downloadCodeSnippet(this)" class="px-2 py-0.5 rounded bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[11px] transition flex items-center gap-1 border border-indigo-200 cursor-pointer font-medium">
                            Tải .java
                        </button>
                    </div>
                `;

                pre.parentNode.insertBefore(wrapper, pre);
                wrapper.appendChild(header);
                if (archBadge) {
                    wrapper.insertAdjacentHTML('beforeend', archBadge);
                }
                wrapper.appendChild(pre);
                pre.className = 'p-3 text-xs overflow-x-auto m-0 bg-slate-50/50 text-slate-800';
            });
        }

        function copyCodeSnippet(btn) {
            const wrapper = btn.closest('.code-toolbar-wrapper');
            const code = wrapper ? wrapper.querySelector('code') : null;
            if (!code) return;
            navigator.clipboard.writeText(code.innerText).then(() => {
                const orig = btn.innerHTML;
                btn.innerHTML = '✓ Đã chép!';
                btn.classList.add('text-emerald-600');
                setTimeout(() => {
                    btn.innerHTML = orig;
                    btn.classList.remove('text-emerald-600');
                }, 2000);
            });
        }

        function downloadCodeSnippet(btn) {
            const wrapper = btn.closest('.code-toolbar-wrapper');
            const code = wrapper ? wrapper.querySelector('code') : null;
            if (!code) return;
            const text = code.innerText;

            let filename = 'CourseManagementCode.java';
            const match = text.match(/(?:public\s+)?(?:class|interface|enum|record)\s+([A-Za-z0-9_]+)/);
            if (match && match[1]) {
                filename = match[1] + '.java';
            }

            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        // ======================================================================
        // STREAMING SEND & RENDER PIPELINE
        // ======================================================================
        async function handleSend(e) {
            if (e) e.preventDefault();
            const inputEl = document.getElementById('user-input');
            const query = inputEl.value.trim();
            if (!query) return;

            inputEl.value = '';
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;

            const chatBox = document.getElementById('chat-box');
            if (document.getElementById('welcome-card')) {
                document.getElementById('welcome-card').remove();
            }

            // User Message Card
            chatBox.insertAdjacentHTML('beforeend', `
                <div class="flex justify-end mb-4">
                    <div class="bg-slate-900 text-white text-sm px-4 py-2.5 rounded-2xl rounded-tr-sm max-w-2xl shadow-sm">
                        <span class="text-xs text-slate-400 block mb-0.5">Yêu cầu của bạn:</span>
                        ${escapeHtml(query)}
                    </div>
                </div>
            `);

            const targetMode = currentMode;
            const containerId = 'resp-' + Date.now();
            const customClaudeKey = localStorage.getItem('cms_anthropic_key') || '';

            try {
                const response = await fetch('/api/chat_stream', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: query,
                        mode: targetMode,
                        anthropic_api_key: customClaudeKey,
                        history: chatHistory.slice(-8)
                    })
                });

                if (!response.ok) {
                    throw new Error('Lỗi máy chủ HTTP: ' + response.status);
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let buffer = '';

                let streamState = {
                    mode: targetMode,
                    prompt: query,
                    hasClaudeApi: false,
                    singleText: '',
                    cols: {
                        base: { text: '', elapsed: 0, eval: null, ragFiles: [] },
                        finetuned: { text: '', elapsed: 0, eval: null, ragFiles: [] },
                        general: { text: '', elapsed: 0, eval: null, ragFiles: [] },
                        project: { text: '', elapsed: 0, eval: null, ragFiles: [] },
                        claude: { text: '', elapsed: 0, eval: null, ragFiles: [] }
                    }
                };

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        const trimmed = line.trim();
                        if (!trimmed.startsWith('data:')) continue;
                        const jsonStr = trimmed.substring(5).trim();
                        if (!jsonStr) continue;

                        try {
                            const evt = JSON.parse(jsonStr);
                            processStreamEvent(evt, containerId, streamState, chatBox);
                            if (evt.type === 'single_chunk' || evt.type === 'init_compare' || evt.type === 'all_done') {
                                chatBox.scrollTop = chatBox.scrollHeight;
                            }
                        } catch (err) {
                            console.error("Lỗi parse SSE:", err, jsonStr);
                        }
                    }
                }

                // Kết thúc: Nâng cấp Code blocks và lưu session
                const containerEl = document.getElementById(containerId);
                if (containerEl) {
                    enhanceCodeBlocks(containerEl);
                }
                saveSession(query, targetMode, chatBox.innerHTML);

            } catch (err) {
                console.error(err);
                chatBox.insertAdjacentHTML('beforeend', `
                    <div class="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-4 rounded-xl mb-4">
                        <strong>Lỗi:</strong> ${err.message}
                    </div>
                `);
            } finally {
                sendBtn.disabled = false;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        function processStreamEvent(evt, containerId, state, chatBox) {
            let container = document.getElementById(containerId);

            // ==========================================
            // CHẾ ĐỘ ĐƠN LẺ (LOCAL / CLOUD / HYBRID)
            // ==========================================
            if (evt.type === 'single_start') {
                const isCloud = evt.source === 'cloud_delegated';
                const badgeClass = isCloud 
                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200' 
                    : 'bg-emerald-50 text-emerald-700 border-emerald-200';
                const ragTags = (evt.rag_files && evt.rag_files.length)
                    ? `<div class="mt-2 pt-2 border-t border-slate-100 flex flex-wrap items-center gap-1.5 text-[11px] text-slate-500">
                           <span class="font-semibold text-slate-600">📂 Nguồn RAG:</span>
                           ${evt.rag_files.map(f => `<span class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-700 font-mono text-[10px]">${escapeHtml(f)}</span>`).join('')}
                       </div>`
                    : '';

                chatBox.insertAdjacentHTML('beforeend', `
                    <div id="${containerId}" class="bg-white border border-slate-200 rounded-xl p-5 mb-5 shadow-sm">
                        <div class="pb-3 mb-3 border-b border-slate-100 text-xs">
                            <div class="flex items-center justify-between flex-wrap gap-2">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full ${isCloud ? 'bg-indigo-500 animate-pulse' : 'bg-emerald-500'}"></span>
                                    <span class="text-xs px-2.5 py-0.5 rounded-full border ${badgeClass} font-semibold">
                                        ${escapeHtml(evt.badge)}
                                    </span>
                                </div>
                                <span id="${containerId}-timer" class="text-slate-400 font-mono text-[11px] animate-pulse">Đang xử lý...</span>
                            </div>
                            ${ragTags}
                        </div>
                        <div id="${containerId}-content" class="prose text-sm text-slate-800 leading-relaxed overflow-x-auto typing-cursor"></div>
                        <div id="${containerId}-eval" class="mt-3"></div>
                    </div>
                `);
                return;
            }

            if (evt.type === 'single_chunk') {
                state.singleText += evt.chunk;
                const contentEl = document.getElementById(`${containerId}-content`);
                if (contentEl) {
                    contentEl.innerHTML = marked.parse(state.singleText);
                }
                return;
            }

            if (evt.type === 'single_done') {
                const timerEl = document.getElementById(`${containerId}-timer`);
                const contentEl = document.getElementById(`${containerId}-content`);
                if (timerEl) {
                    timerEl.classList.remove('animate-pulse');
                    timerEl.textContent = `${evt.elapsed}s`;
                }
                if (contentEl) {
                    contentEl.classList.remove('typing-cursor');
                    contentEl.innerHTML = marked.parse(state.singleText);
                }
                if (evt.eval) {
                    const evalEl = document.getElementById(`${containerId}-eval`);
                    if (evalEl) evalEl.innerHTML = renderEvalScorecard(evt.eval);
                }
                chatHistory.push({ role: 'user', content: state.prompt });
                chatHistory.push({ role: 'assistant', content: state.singleText });
                if (chatHistory.length > 10) chatHistory = chatHistory.slice(-8);
                return;
            }

            // ==========================================
            // CHẾ ĐỘ SO SÁNH (COMPARE MODELS / SYSTEM / ARENA / CLAUDE)
            // ==========================================
            if (evt.type === 'init_compare') {
                state.hasClaudeApi = Boolean(evt.has_claude_api);
                let columnsHtml = '';
                if (evt.mode === 'compare_models') {
                    columnsHtml = `
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                            <div class="bg-white border border-amber-200 rounded-xl p-4 flex flex-col shadow-sm">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-amber-100 text-xs">
                                    <span class="font-bold text-amber-800 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-amber-500"></span> Base Model (Chưa Fine-tune)
                                    </span>
                                    <span id="${containerId}-base-time" class="text-amber-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-base-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-base-eval" class="mt-3"></div>
                            </div>
                            <div class="bg-white border border-emerald-300 rounded-xl p-4 flex flex-col shadow-sm ring-1 ring-emerald-100">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-100 text-xs">
                                    <span class="font-bold text-emerald-800 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Fine-tuned + RAG (LoRA GPU)
                                    </span>
                                    <span id="${containerId}-finetuned-time" class="text-emerald-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-finetuned-rag" class="mb-2"></div>
                                <div id="${containerId}-finetuned-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-finetuned-eval" class="mt-3"></div>
                            </div>
                        </div>
                    `;
                } else if (evt.mode === 'compare_system') {
                    columnsHtml = `
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                            <div class="bg-white border border-slate-200 rounded-xl p-4 flex flex-col shadow-sm">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-100 text-xs">
                                    <span class="font-bold text-slate-800 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-slate-400"></span> AI Tiêu Chuẩn (Zero Context)
                                    </span>
                                    <span id="${containerId}-general-time" class="text-slate-600 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-general-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-general-eval" class="mt-3"></div>
                            </div>
                            <div class="bg-white border border-emerald-300 rounded-xl p-4 flex flex-col shadow-sm ring-1 ring-emerald-100">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-100 text-xs">
                                    <span class="font-bold text-emerald-800 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Hệ Thống Dự Án (LoRA + RAG)
                                    </span>
                                    <span id="${containerId}-project-time" class="text-emerald-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-project-rag" class="mb-2"></div>
                                <div id="${containerId}-project-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-project-eval" class="mt-3"></div>
                            </div>
                        </div>
                    `;
                } else if (evt.mode === 'compare_arena') {
                    columnsHtml = `
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-start">
                            <div class="bg-white border border-slate-200 rounded-xl p-4 flex flex-col shadow-sm">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-100 text-xs">
                                    <span class="font-bold text-slate-800 flex items-center gap-1">🌐 AI Tiêu Chuẩn (Zero Context)</span>
                                    <span id="${containerId}-general-time" class="text-slate-600 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-general-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-general-eval" class="mt-3"></div>
                            </div>
                            <div class="bg-white border border-amber-200 rounded-xl p-4 flex flex-col shadow-sm">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-amber-100 text-xs">
                                    <span class="font-bold text-amber-800 flex items-center gap-1">💻 Base Model (GPU)</span>
                                    <span id="${containerId}-base-time" class="text-amber-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-base-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-base-eval" class="mt-3"></div>
                            </div>
                            <div class="bg-white border border-emerald-300 rounded-xl p-4 flex flex-col shadow-sm ring-1 ring-emerald-100">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-100 text-xs">
                                    <span class="font-bold text-emerald-800 flex items-center gap-1">🏆 Fine-tuned + RAG (GPU)</span>
                                    <span id="${containerId}-finetuned-time" class="text-emerald-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-finetuned-rag" class="mb-2"></div>
                                <div id="${containerId}-finetuned-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                                <div id="${containerId}-finetuned-eval" class="mt-3"></div>
                            </div>
                        </div>
                    `;
                } else if (evt.mode === 'compare_claude') {
                    const autoClaude = Boolean(evt.has_claude_api);
                    const claudePanelHtml = autoClaude
                        ? `<div id="${containerId}-claude-body" class="prose text-xs text-slate-700 leading-relaxed overflow-y-auto overflow-x-auto max-h-[460px] pr-1"></div>
                           <div id="${containerId}-claude-eval" class="mt-3"></div>`
                        : `<div class="space-y-2.5 flex-1 flex flex-col">
                               <div class="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-[11px] text-slate-600 leading-relaxed">
                                   Chưa cấu hình <code>ANTHROPIC_API_KEY</code>. Hãy bấm <strong>Copy Prompt</strong> dán sang <strong>claude.ai</strong>, rồi dán câu trả lời của Claude vào ô dưới để chấm điểm 5 tiêu chí kiến trúc:
                               </div>
                               <div class="flex items-center gap-2">
                                   <button type="button" onclick="copyClaudePrompt('${containerId}')"
                                           class="px-2.5 py-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-50 text-[11px] font-medium text-slate-700 cursor-pointer">
                                       📋 Copy Prompt Gửi Claude.ai
                                   </button>
                                   <button type="button" onclick="scorePastedClaude('${containerId}')"
                                           class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-[11px] font-medium text-white cursor-pointer">
                                       ⚖️ Chấm Điểm Đối Chiếu
                                   </button>
                               </div>
                               <textarea id="${containerId}-claude-paste" rows="8"
                                         placeholder="Dán nguyên văn câu trả lời (hoặc code Java) từ Claude.ai vào đây..."
                                         class="w-full flex-1 bg-white border border-slate-300 rounded-lg p-2.5 text-xs font-mono text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"></textarea>
                               <div id="${containerId}-claude-eval"></div>
                               <details class="text-[11px] text-slate-500 pt-1">
                                   <summary class="cursor-pointer hover:text-slate-700 font-medium">Tùy chọn: Nhập Anthropic API Key để gọi trực tiếp</summary>
                                   <div class="mt-2 flex gap-1.5">
                                       <input id="${containerId}-claude-key-input" type="password" placeholder="sk-ant-..."
                                              class="flex-1 border border-slate-300 rounded px-2 py-1 text-xs">
                                       <button type="button" onclick="saveClaudeSessionKey('${containerId}')"
                                               class="px-2.5 py-1 bg-indigo-600 text-white rounded text-xs cursor-pointer">Lưu</button>
                                   </div>
                               </details>
                           </div>`;

                    columnsHtml = `
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4" data-prompt="${escapeHtml(state.prompt)}">
                            <div class="bg-white border border-emerald-300 rounded-xl p-4 flex flex-col shadow-sm ring-1 ring-emerald-100">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-100 text-xs">
                                    <span class="font-bold text-emerald-800 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> Hệ Thống Dự Án (LoRA + RAG)
                                    </span>
                                    <span id="${containerId}-project-time" class="text-emerald-700 font-mono">Đang chờ...</span>
                                </div>
                                <div id="${containerId}-project-rag" class="mb-2"></div>
                                <div id="${containerId}-project-body" class="prose text-xs text-slate-700 leading-relaxed overflow-x-auto flex-1"></div>
                                <div id="${containerId}-project-eval" class="mt-3"></div>
                            </div>
                            <div class="bg-white border border-violet-200 rounded-xl p-4 flex flex-col shadow-sm">
                                <div class="flex items-center justify-between pb-2 mb-2 border-b border-violet-100 text-xs">
                                    <span class="font-bold text-violet-900 flex items-center gap-1.5">
                                        <span class="w-2 h-2 rounded-full bg-violet-500"></span> Claude (Zero-Context Baseline)
                                    </span>
                                    <span id="${containerId}-claude-time" class="text-violet-700 font-mono">${autoClaude ? 'Đang chờ...' : 'Chờ paste câu trả lời'}</span>
                                </div>
                                ${claudePanelHtml}
                            </div>
                        </div>
                    `;
                }

                chatBox.insertAdjacentHTML('beforeend', `
                    <div id="${containerId}" class="mb-5">
                        <div class="bg-slate-100 border border-slate-200 rounded-lg p-2.5 mb-3 text-xs text-slate-700 flex items-center justify-between">
                            <span class="font-bold">${escapeHtml(evt.title)}</span>
                            <span id="${containerId}-status" class="text-indigo-600 animate-pulse font-medium">Đang truyền phát mã nguồn song song...</span>
                        </div>
                        ${columnsHtml}
                        <div id="${containerId}-summary" class="mt-3"></div>
                    </div>
                `);
                window[`__state_${containerId}`] = state;
                return;
            }

            if (evt.type === 'col_start') {
                const statusEl = document.getElementById(`${containerId}-status`);
                if (statusEl && evt.title) {
                    statusEl.textContent = `Đang chạy: ${evt.title}...`;
                }
                const timer = document.getElementById(`${containerId}-${evt.col}-time`);
                if (timer) {
                    timer.classList.add('animate-pulse');
                    timer.textContent = 'Đang sinh...';
                }
                if (evt.rag_files && evt.rag_files.length) {
                    const ragBox = document.getElementById(`${containerId}-${evt.col}-rag`);
                    if (ragBox) {
                        ragBox.innerHTML = `<div class="flex flex-wrap items-center gap-1 text-[10px] text-slate-500 bg-slate-50 border border-slate-200/80 rounded-lg px-2 py-1">
                            <span class="font-semibold text-slate-600">📂 RAG:</span>
                            ${evt.rag_files.map(f => `<span class="px-1.5 py-0.2 rounded bg-white border border-slate-200 text-slate-700 font-mono">${escapeHtml(f)}</span>`).join('')}
                        </div>`;
                    }
                }
                return;
            }

            if (evt.type === 'col_chunk') {
                if (state.cols[evt.col]) {
                    state.cols[evt.col].text += evt.chunk;
                    const el = document.getElementById(`${containerId}-${evt.col}-body`);
                    if (el) {
                        el.innerHTML = marked.parse(state.cols[evt.col].text);
                        el.scrollTop = el.scrollHeight;
                    }
                }
                return;
            }

            if (evt.type === 'col_done') {
                if (state.cols[evt.col]) {
                    state.cols[evt.col].elapsed = evt.elapsed;
                    state.cols[evt.col].eval = evt.eval || null;
                    const timer = document.getElementById(`${containerId}-${evt.col}-time`);
                    if (timer) {
                        timer.classList.remove('animate-pulse');
                        timer.textContent = `✓ ${evt.elapsed}s`;
                    }
                    const evalEl = document.getElementById(`${containerId}-${evt.col}-eval`);
                    if (evalEl && evt.eval) {
                        evalEl.innerHTML = `
                            <div class="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-2 text-[11px] text-slate-500 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
                                <span>Đã sinh xong (${evt.elapsed}s) — Chờ các mô hình còn lại hoàn tất để chấm điểm đồng bộ...</span>
                            </div>
                        `;
                    }
                }
                return;
            }

            if (evt.type === 'all_done') {
                const status = document.getElementById(`${containerId}-status`);
                if (status) {
                    status.classList.remove('animate-pulse');
                    status.classList.add('text-slate-600');
                    status.textContent = `Hoàn tất & Đã chấm điểm (${evt.total_elapsed}s)`;
                }
                Object.entries(state.cols).forEach(([colKey, colState]) => {
                    const bodyEl = document.getElementById(`${containerId}-${colKey}-body`);
                    if (bodyEl) {
                        bodyEl.scrollTop = 0;
                    }
                    if (colState && colState.eval) {
                        const evalEl = document.getElementById(`${containerId}-${colKey}-eval`);
                        if (evalEl) {
                            evalEl.innerHTML = renderEvalScorecard(colState.eval);
                        }
                    }
                });
                renderComparisonSummary(containerId, state);
                return;
            }
        }

        function renderEvalScorecard(ev) {
            if (!ev) return '';
            if (ev.api_error) {
                return `
                    <div class="rounded-lg border border-amber-300 bg-amber-50 p-2.5 text-[11px] text-amber-900">
                        <div class="flex items-center justify-between font-semibold mb-0.5">
                            <span>⚠️ Cloud API không phản hồi</span>
                            <span class="px-2 py-0.5 rounded bg-amber-600 text-white font-mono text-[10px]">N/A</span>
                        </div>
                        <div class="opacity-85">${escapeHtml(ev.task_label || 'Không chấm điểm do lỗi kết nối/quota API')}</div>
                    </div>
                `;
            }
            const score = ev.score || 0;
            const tone = score >= 80
                ? { box: 'bg-emerald-50 border-emerald-200', badge: 'bg-emerald-600 text-white', text: 'text-emerald-900' }
                : (score >= 50
                    ? { box: 'bg-amber-50 border-amber-200', badge: 'bg-amber-600 text-white', text: 'text-amber-900' }
                    : { box: 'bg-rose-50 border-rose-200', badge: 'bg-rose-600 text-white', text: 'text-rose-900' });

            const chips = (ev.criteria || []).map(c => {
                const cls = c.passed
                    ? 'bg-white border-emerald-300 text-emerald-800'
                    : 'bg-white/70 border-slate-200 text-slate-400 line-through';
                return `<span class="px-1.5 py-0.5 rounded border text-[10px] font-medium ${cls}">${c.passed ? '✓' : '✗'} ${escapeHtml(c.name)}</span>`;
            }).join('');

            return `
                <div class="rounded-lg border p-2.5 ${tone.box}">
                    <div class="flex items-center justify-between text-[11px] font-semibold ${tone.text} mb-1">
                        <span>🎯 Điểm Tuân Thủ Kiến Trúc CMS</span>
                        <span class="px-2 py-0.5 rounded font-mono text-[11px] ${tone.badge}">${score}/100 (${ev.passed_count}/${ev.total})</span>
                    </div>
                    ${ev.task_label ? `<div class="text-[10px] opacity-80 mb-1.5 font-medium">${escapeHtml(ev.task_label)}</div>` : ''}
                    <div class="flex flex-wrap gap-1">${chips}</div>
                </div>
            `;
        }

        function renderComparisonSummary(containerId, state) {
            const summaryEl = document.getElementById(`${containerId}-summary`);
            if (!summaryEl) return;
            const labels = {
                general: 'AI Tiêu Chuẩn (Zero-Context)',
                base: 'Base Model (GPU)',
                finetuned: 'Fine-tuned + RAG (LoRA GPU)',
                project: 'Hệ Thống Dự Án (LoRA + RAG)',
                claude: 'Claude'
            };
            const allEntries = Object.entries(state.cols)
                .filter(([, v]) => v && v.eval)
                .map(([k, v]) => ({ key: k, label: labels[k] || k, score: v.eval.score, apiError: Boolean(v.eval.api_error), elapsed: v.elapsed }));
            const validEntries = allEntries.filter(e => !e.apiError);
            if (!validEntries.length) return;
            if (allEntries.length < 2) return;

            const best = [...validEntries].sort((a, b) => b.score - a.score || a.elapsed - b.elapsed)[0];
            summaryEl.innerHTML = `
                <div class="bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2.5 text-xs flex flex-wrap items-center justify-between gap-2">
                    <span class="font-semibold text-slate-800">🏆 Kết Luận Đối Chiếu: <span class="text-emerald-700">${escapeHtml(best.label)}</span> dẫn đầu với <strong>${best.score}/100 điểm</strong> (${best.elapsed}s)</span>
                    <span class="text-[11px] text-slate-500">${allEntries.map(e => `${escapeHtml(e.label)}: ${e.apiError ? 'Lỗi API' : e.score + '%'}`).join(' • ')}</span>
                </div>
            `;
        }

        function copyClaudePrompt(containerId) {
            const st = window[`__state_${containerId}`];
            const promptText = st ? st.prompt : '';
            if (!promptText) return;
            navigator.clipboard.writeText(promptText).then(() => {
                showToast("Đã copy prompt — hãy dán vào Claude.ai!", "✓");
            });
        }

        function saveClaudeSessionKey(containerId) {
            const inp = document.getElementById(`${containerId}-claude-key-input`);
            if (!inp) return;
            const val = inp.value.trim();
            if (val) {
                localStorage.setItem('cms_anthropic_key', val);
                showToast("Đã lưu Anthropic API Key cho trình duyệt này", "✓");
            } else {
                localStorage.removeItem('cms_anthropic_key');
                showToast("Đã xóa API Key khỏi trình duyệt", "✓");
            }
        }

        async function scorePastedClaude(containerId) {
            const ta = document.getElementById(`${containerId}-claude-paste`);
            const evalEl = document.getElementById(`${containerId}-claude-eval`);
            if (!ta || !evalEl) return;
            const text = ta.value.trim();
            if (!text) {
                showToast("Vui lòng dán câu trả lời của Claude vào trước", "⚠️");
                return;
            }
            const st = window[`__state_${containerId}`];
            const res = await fetch('/api/score_response', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text, prompt: st ? st.prompt : '' })
            });
            const data = await res.json();
            if (data.eval) {
                evalEl.innerHTML = renderEvalScorecard(data.eval);
                const st = window[`__state_${containerId}`];
                if (st) {
                    st.cols.claude.text = text;
                    st.cols.claude.eval = data.eval;
                    renderComparisonSummary(containerId, st);
                }
                showToast(`Đã chấm điểm Claude: ${data.eval.score}/100`, "⚖️");
            }
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        document.addEventListener('click', (e) => {
            const popup = document.getElementById('action-menu-popup');
            const btn = document.getElementById('btn-action-menu');
            if (popup && !popup.classList.contains('hidden')) {
                if (!popup.contains(e.target) && !btn.contains(e.target)) {
                    closeActionMenu();
                }
            }

            const cmpPopup = document.getElementById('compare-menu-popup');
            const cmpBtn = document.getElementById('btn-compare-menu');
            if (cmpPopup && !cmpPopup.classList.contains('hidden')) {
                if (!cmpPopup.contains(e.target) && !cmpBtn.contains(e.target)) {
                    closeCompareMenu();
                }
            }
        });

        window.addEventListener('DOMContentLoaded', () => {
            renderHistorySidebar();
            filterActions('', 'all');
            updateCompareMenuUI(currentMode);
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        has_claude_key=bool(anthropic_api_key),
        has_openrouter_key=bool(openrouter_api_key),
        rag_count=len(rag_engine.docs)
    )


@app.route("/api/rag/refresh", methods=["POST"])
def refresh_rag():
    count = rag_engine.refresh()
    return jsonify({"status": "ok", "indexed_files": count})


@app.route("/api/score_response", methods=["POST"])
def score_response():
    data = request.json or {}
    text = data.get("text", "")
    prompt_text = data.get("prompt", "")
    return jsonify({"eval": evaluate_architecture_compliance(text, prompt_text)})


@app.route("/benchmark-report")
def benchmark_report():
    report_path = os.path.join(root_dir, "benchmark", "bao_cao_truc_quan.html")
    if not os.path.exists(report_path):
        report_path = os.path.join(root_dir, "bao_cao_truc_quan.html")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Chưa tìm thấy file bao_cao_truc_quan.html. Vui lòng chạy benchmark_comparison.py trước!", 404

# ======================================================================
# API CHAT STREAMING (SERVER-SENT EVENTS - SSE)
# ======================================================================
@app.route("/api/chat_stream", methods=["POST"])
def chat_stream():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    mode = data.get("mode", "hybrid")
    req_claude_key = (data.get("anthropic_api_key") or "").strip()
    chat_history = data.get("history") or []

    if not user_message:
        def err_stream():
            yield f"data: {json.dumps({'type': 'error', 'message': 'Vui lòng nhập câu hỏi'})}\n\n"
        return Response(stream_with_context(err_stream()), mimetype="text/event-stream")

    def sse_generator():
        start_time = time.time()
        rag_block, rag_files = retrieve_rag_for_query(user_message, top_k=3, max_chars=1800)
        effective_claude_key = req_claude_key or anthropic_api_key

        try:
            # 1. Chế độ SO SÁNH MODEL: Base Model vs Fine-tuned + RAG (Local GPU)
            if mode == "compare_models":
                yield f"data: {json.dumps({'type': 'init_compare', 'mode': 'compare_models', 'title': '⚖️ SO SÁNH TRỰC DIỆN MODEL TRÊN GPU (RTX 4050)'})}\n\n"

                # Cột 1: Base Model (không LoRA, không RAG -> đánh giá công bằng nguyên bản)
                col1_start = time.time()
                buf_base = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'base', 'title': f'Mô hình Gốc ({base_model_id} GPU)'})}\n\n"
                for chunk in generate_local_stream(user_message, use_adapter=False, max_tokens=1000, use_rag=False):
                    buf_base.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'base', 'chunk': chunk})}\n\n"
                t_base = round(time.time() - col1_start, 2)
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'base', 'elapsed': t_base, 'eval': evaluate_architecture_compliance(''.join(buf_base), user_message)})}\n\n"

                # Cột 2: Fine-tuned Model + RAG
                col2_start = time.time()
                buf_ft = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'finetuned', 'title': 'Mô hình Fine-tuned + RAG (LoRA GPU)', 'rag_files': rag_files})}\n\n"
                for chunk in generate_local_stream(user_message, use_adapter=True, max_tokens=1200, use_rag=True, rag_context=rag_block):
                    buf_ft.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'finetuned', 'chunk': chunk})}\n\n"
                t_ft = round(time.time() - col2_start, 2)
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'finetuned', 'elapsed': t_ft, 'eval': evaluate_architecture_compliance(''.join(buf_ft), user_message)})}\n\n"

                yield f"data: {json.dumps({'type': 'all_done', 'total_elapsed': round(time.time() - start_time, 2)})}\n\n"
                return

            # 2. Chế độ SO SÁNH HỆ THỐNG: Dự Án vs AI Tiêu Chuẩn (Zero Context)
            if mode == "compare_system":
                yield f"data: {json.dumps({'type': 'init_compare', 'mode': 'compare_system', 'title': '🏆 ĐỐI ĐẦU HỆ THỐNG: DỰ ÁN VS AI TIÊU CHUẨN'})}\n\n"

                c1_start = time.time()
                buf_gen = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'general', 'title': 'AI Tiêu Chuẩn Bên Ngoài (Zero Context)'})}\n\n"
                for chunk in call_cloud_general_ai_stream(user_message, claude_key=effective_claude_key):
                    buf_gen.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'general', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'general', 'elapsed': round(time.time() - c1_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_gen), user_message)})}\n\n"

                c2_start = time.time()
                buf_proj = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'project', 'title': 'Hệ Thống AI Của Dự Án (LoRA + RAG)', 'rag_files': rag_files})}\n\n"
                streamer = generate_local_stream(user_message, use_adapter=True, max_tokens=1200, use_rag=True, rag_context=rag_block) if local_ready else call_cloud_gemini_stream(user_message)
                for chunk in streamer:
                    buf_proj.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'project', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'project', 'elapsed': round(time.time() - c2_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_proj), user_message)})}\n\n"

                yield f"data: {json.dumps({'type': 'all_done', 'total_elapsed': round(time.time() - start_time, 2)})}\n\n"
                return

            # 3. Chế độ ĐẤU TRƯỜNG 3 CHIỀU
            if mode == "compare_arena":
                yield f"data: {json.dumps({'type': 'init_compare', 'mode': 'compare_arena', 'title': '📊 ĐẤU TRƯỜNG 3 CHIỀU'})}\n\n"

                c1_start = time.time()
                buf_gen = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'general', 'title': 'AI Tiêu Chuẩn (Zero Context)'})}\n\n"
                for chunk in call_cloud_general_ai_stream(user_message, claude_key=effective_claude_key):
                    buf_gen.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'general', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'general', 'elapsed': round(time.time() - c1_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_gen), user_message)})}\n\n"

                c2_start = time.time()
                buf_base = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'base', 'title': f'Base Model ({base_model_id} GPU)'})}\n\n"
                for chunk in generate_local_stream(user_message, use_adapter=False, max_tokens=1000, use_rag=False):
                    buf_base.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'base', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'base', 'elapsed': round(time.time() - c2_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_base), user_message)})}\n\n"

                c3_start = time.time()
                buf_ft = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'finetuned', 'title': 'Fine-tuned + RAG (Local GPU)', 'rag_files': rag_files})}\n\n"
                for chunk in generate_local_stream(user_message, use_adapter=True, max_tokens=1200, use_rag=True, rag_context=rag_block):
                    buf_ft.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'finetuned', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'finetuned', 'elapsed': round(time.time() - c3_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_ft), user_message)})}\n\n"

                yield f"data: {json.dumps({'type': 'all_done', 'total_elapsed': round(time.time() - start_time, 2)})}\n\n"
                return

            # 4. Chế độ SO SÁNH VỚI CLAUDE
            if mode == "compare_claude":
                has_key = bool(effective_claude_key)
                yield f"data: {json.dumps({'type': 'init_compare', 'mode': 'compare_claude', 'title': '🤖 ĐỐI CHIẾU TRỰC TIẾP VỚI CLAUDE', 'has_claude_api': has_key})}\n\n"

                c_proj_start = time.time()
                buf_proj = []
                yield f"data: {json.dumps({'type': 'col_start', 'col': 'project', 'title': 'Hệ Thống Dự Án (LoRA + RAG)', 'rag_files': rag_files})}\n\n"
                streamer = generate_local_stream(user_message, use_adapter=True, max_tokens=1200, use_rag=True, rag_context=rag_block) if local_ready else call_cloud_gemini_stream(user_message)
                for chunk in streamer:
                    buf_proj.append(chunk)
                    yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'project', 'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'col_done', 'col': 'project', 'elapsed': round(time.time() - c_proj_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_proj), user_message)})}\n\n"

                if has_key:
                    c_claude_start = time.time()
                    buf_claude = []
                    yield f"data: {json.dumps({'type': 'col_start', 'col': 'claude', 'title': 'Claude (Anthropic API)'})}\n\n"
                    for chunk in call_claude_stream(user_message, api_key=effective_claude_key, system_prompt=SYSTEM_INSTRUCTION_GENERAL):
                        buf_claude.append(chunk)
                        yield f"data: {json.dumps({'type': 'col_chunk', 'col': 'claude', 'chunk': chunk})}\n\n"
                    yield f"data: {json.dumps({'type': 'col_done', 'col': 'claude', 'elapsed': round(time.time() - c_claude_start, 2), 'eval': evaluate_architecture_compliance(''.join(buf_claude), user_message)})}\n\n"

                yield f"data: {json.dumps({'type': 'all_done', 'total_elapsed': round(time.time() - start_time, 2)})}\n\n"
                return

            # 5. CHẾ ĐỘ ĐƠN LẺ: LOCAL, OPENROUTER, CLOUD, HOẶC HYBRID
            buf_single = []

            if mode == "openrouter":
                _, cloud_rag_files = retrieve_rag_for_query(user_message, top_k=5, max_chars=5000)
                badge = "🚀 DeepSeek-V3 via OpenRouter (Ngữ Cảnh Codebase RAG)"
                source = "openrouter_direct"
                yield f"data: {json.dumps({'type': 'single_start', 'badge': badge, 'source': source, 'rag_files': cloud_rag_files})}\n\n"
                prompt_or = _build_cloud_project_prompt(user_message, history=chat_history)
                for chunk in call_openrouter_stream(prompt_or, model="deepseek/deepseek-chat"):
                    buf_single.append(chunk)
                    yield f"data: {json.dumps({'type': 'single_chunk', 'chunk': chunk})}\n\n"
                elapsed = round(time.time() - start_time, 2)
                yield f"data: {json.dumps({'type': 'single_done', 'elapsed': elapsed, 'eval': evaluate_architecture_compliance(''.join(buf_single), user_message)})}\n\n"
                return

            is_heavy = is_heavy_task(user_message)
            use_cloud = (mode == "cloud") or (mode == "hybrid" and (is_heavy or not local_ready))

            if use_cloud:
                _, cloud_rag_files = retrieve_rag_for_query(user_message, top_k=5, max_chars=5000)
                badge = "🌐 Google Gemini Cloud (Ngữ Cảnh Codebase RAG • 1M Context)" if mode == "cloud" else \
                       ("🌐 Local AI đã phân tích & Ủy quyền cho Cloud AI sinh toàn bộ dự án lớn" if is_heavy else "🌐 Cloud AI phục vụ với Ngữ cảnh Codebase Chuẩn")
                source = "cloud_delegated"
                yield f"data: {json.dumps({'type': 'single_start', 'badge': badge, 'source': source, 'rag_files': cloud_rag_files})}\n\n"
                for chunk in call_cloud_gemini_stream(user_message, history=chat_history):
                    buf_single.append(chunk)
                    yield f"data: {json.dumps({'type': 'single_chunk', 'chunk': chunk})}\n\n"
            else:
                badge = f"⚡ Xử lý 100% Cục bộ trên GPU RTX 4050 ({base_model_id} + LoRA + RAG)"
                source = "local_direct"
                yield f"data: {json.dumps({'type': 'single_start', 'badge': badge, 'source': source, 'rag_files': rag_files})}\n\n"
                for chunk in generate_local_stream(user_message, use_adapter=True, max_tokens=1500, use_rag=True, rag_context=rag_block, history=chat_history):
                    buf_single.append(chunk)
                    yield f"data: {json.dumps({'type': 'single_chunk', 'chunk': chunk})}\n\n"

            elapsed = round(time.time() - start_time, 2)
            yield f"data: {json.dumps({'type': 'single_done', 'elapsed': elapsed, 'eval': evaluate_architecture_compliance(''.join(buf_single), user_message)})}\n\n"

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        finally:
            if has_cuda:
                torch.cuda.empty_cache()

    return Response(stream_with_context(sse_generator()), mimetype="text/event-stream")

# ======================================================================
# API CHAT TRUYỀN THỐNG (FALLBACK ĐỒNG BỘ)
# ======================================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    mode = data.get("mode", "hybrid")

    if not user_message:
        return jsonify({"answer": "Vui lòng nhập câu hỏi hoặc yêu cầu chức năng.", "elapsed": 0.0, "source": "system"}), 400

    try:
        if mode == "compare_models":
            ans_base, time_base = generate_local(user_message, use_adapter=False, max_tokens=250)
            ans_ft, time_ft = generate_local(user_message, use_adapter=True, max_tokens=250)
            return jsonify({
                "mode": "compare_models",
                "base": {"title": f"Mô hình Gốc ({base_model_id} GPU)", "answer": ans_base, "elapsed": time_base},
                "finetuned": {"title": f"Mô hình Fine-tuned (LoRA GPU)", "answer": ans_ft, "elapsed": time_ft}
            })

        if mode == "local":
            ans, elapsed = generate_local(user_message, use_adapter=True, max_tokens=1500)
            return jsonify({
                "answer": ans,
                "elapsed": elapsed,
                "source": "local_direct",
                "badge": f"⚡ Xử lý 100% Cục bộ trên GPU RTX 4050 ({base_model_id} + LoRA)"
            })

        if mode == "cloud":
            ans, elapsed = call_cloud_gemini(user_message)
            return jsonify({
                "answer": ans,
                "elapsed": elapsed,
                "source": "cloud_delegated",
                "badge": "🌐 Google Gemini Cloud (Ngữ Cảnh Kiến Trúc Codebase • 1M Context)"
            })

        if mode == "openrouter":
            prompt_or = _build_cloud_project_prompt(user_message)
            start_t = time.time()
            chunks = list(call_openrouter_stream(prompt_or, model="deepseek/deepseek-chat"))
            ans = "".join(chunks)
            elapsed = round(time.time() - start_t, 2)
            return jsonify({
                "answer": ans,
                "elapsed": elapsed,
                "source": "openrouter_direct",
                "badge": "🚀 DeepSeek-V3 via OpenRouter (Ngữ Cảnh Codebase RAG)"
            })

        if mode == "compare_system":
            ans_gen, time_gen = call_cloud_general_ai(user_message)
            ans_proj, time_proj = generate_local(user_message, use_adapter=True, max_tokens=600)
            if not local_ready:
                ans_proj, time_proj = call_cloud_gemini(user_message)
            return jsonify({
                "mode": "compare_system",
                "general": {"title": "AI Tiêu Chuẩn Bên Ngoài (Zero Context)", "answer": ans_gen, "elapsed": time_gen},
                "project": {"title": "Hệ Thống AI Của Dự Án (GPU RTX 4050)", "answer": ans_proj, "elapsed": time_proj}
            })

        if mode == "compare_arena":
            ans_gen, time_gen = call_cloud_general_ai(user_message)
            ans_base, time_base = generate_local(user_message, use_adapter=False, max_tokens=800)
            ans_ft, time_ft = generate_local(user_message, use_adapter=True, max_tokens=800)
            return jsonify({
                "mode": "compare_arena",
                "general": {"title": "AI Tiêu Chuẩn (Zero-Context)", "answer": ans_gen, "elapsed": time_gen},
                "base": {"title": f"Base Model ({base_model_id} GPU)", "answer": ans_base, "elapsed": time_base},
                "finetuned": {"title": "Fine-tuned Model (Local GPU)", "answer": ans_ft, "elapsed": time_ft}
            })

        is_heavy = is_heavy_task(user_message)
        if is_heavy or not local_ready:
            ans, elapsed = call_cloud_gemini(user_message)
            badge_title = "🌐 Local AI đã phân tích & Ủy quyền cho Cloud AI sinh toàn bộ dự án lớn" if is_heavy else "🌐 Cloud AI phục vụ với Ngữ cảnh Codebase Chuẩn"
            return jsonify({"answer": ans, "elapsed": elapsed, "source": "cloud_delegated", "badge": badge_title})
        else:
            ans, elapsed = generate_local(user_message, use_adapter=True, max_tokens=1500)
            return jsonify({"answer": ans, "elapsed": elapsed, "source": "local_direct", "badge": f"⚡ Tự xử lý trực tiếp bởi Local AI ({base_model_id} trên GPU RTX 4050)"})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"answer": f"Đã xảy ra lỗi: {str(e)}", "elapsed": 0.0, "source": "error", "badge": "⚠️ Lỗi xử lý"}), 200

if __name__ == "__main__":
    port = 7860
    print(f"\n=======================================================")
    print(f"WEB CHATBOT HYBRID & SO SÁNH STREAMING ĐÃ SẴN SÀNG TẠI: http://localhost:{port}")
    print(f"Trình duyệt web sẽ tự động mở trong giây lát...")
    print(f"=======================================================\n")
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    if os.environ.get("AUTO_OPEN_BROWSER", "true").lower() == "true" and os.name == "nt":
        threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(host=host, port=port, debug=False)
