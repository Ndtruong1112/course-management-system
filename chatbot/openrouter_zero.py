"""OpenRouter baseline that sends only the user's current prompt."""

import json

import requests


ZERO_CONTEXT_MODELS = {
    "particle-ai/particle-1:free": "Particle-1 (coding)",
    "cohere/north-mini-code:free": "North Mini Code (coding)",
    "recursive/flint-v1.0:free": "Flint (coding)",
    "nvidia/nemotron-3.5-lightning:free": "Nemotron 3.5 Lightning",
    "openrouter/free": "Free Router (model ngẫu nhiên)",
}
DEFAULT_ZERO_MODEL = "particle-ai/particle-1:free"


def stream_zero_context(message, model, api_key, post=None, generation_info=None):
    """Do not add repository context, chat history, or automatic model fallbacks."""
    info = generation_info if generation_info is not None else {}
    info.update({"finish_reason": "unknown", "max_new_tokens": 4096})
    if not isinstance(model, str) or model not in ZERO_CONTEXT_MODELS:
        info["finish_reason"] = "error"
        yield "⚠️ Model zero-context không hợp lệ."
        return
    if not api_key:
        info["finish_reason"] = "error"
        yield "⚠️ Chưa cấu hình OPENROUTER_API_KEY trong .env hoặc biến môi trường."
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "Course Management Studio",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "stream": True,
        "max_tokens": 4096,
        "temperature": 0.2,
    }
    response = None
    yielded = False
    try:
        response = (post or requests.post)(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, stream=True, timeout=(10, 90),
        )
        if response.status_code != 200:
            info["finish_reason"] = "error"
            status = response.status_code
            if status in (401, 403):
                yield f"⚠️ OpenRouter từ chối API key hoặc quyền truy cập (HTTP {status})."
            elif status == 429:
                yield "⚠️ OpenRouter đang giới hạn lượt gọi hoặc hết quota miễn phí (HTTP 429)."
            else:
                yield f"⚠️ Model đã chọn không khả dụng hoặc OpenRouter gặp lỗi (HTTP {status})."
            return

        yielded = False
        saw_done = False
        for raw_line in response.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8", errors="replace")
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                saw_done = True
                break
            try:
                event = json.loads(data)
            except json.JSONDecodeError:
                continue
            if event.get("error"):
                info["finish_reason"] = "error"
                yield "⚠️ OpenRouter báo lỗi khi đang tạo phản hồi."
                return
            choices = event.get("choices") or []
            if choices:
                reason = choices[0].get("finish_reason")
                if reason:
                    info["finish_reason"] = reason if reason in ("stop", "length") else "filtered"
                content = (choices[0].get("delta") or {}).get("content")
                if isinstance(content, str) and content:
                    yielded = True
                    yield content
        if not yielded:
            info["finish_reason"] = "error"
            yield "⚠️ Model không trả về nội dung. Vui lòng thử lại hoặc chọn model khác."
        elif not saw_done and info["finish_reason"] == "unknown":
            info["finish_reason"] = "interrupted"
    except requests.RequestException:
        info["finish_reason"] = "interrupted" if yielded else "error"
        if not yielded:
            yield "⚠️ Không thể kết nối OpenRouter hoặc kết nối đã hết thời gian."
    finally:
        if response is not None:
            response.close()
