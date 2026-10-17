import os
import sys
import time
import torch
from flask import Flask, request, jsonify, render_template_string
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Paths
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lora_dir = os.path.join(root_dir, "outputs", "course-management-lora-adapter")
base_model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

print("=" * 70)
print("KHỞI CHẠY DUAL-CHATBOT WEB UI (BASE vs FINE-TUNED)")
print("=" * 70)

has_cuda = torch.cuda.is_available()
gpu_name = torch.cuda.get_device_name(0) if has_cuda else "CPU (Không có GPU)"
print(f"Thiết bị: {gpu_name}")

if not os.path.exists(lora_dir):
    print(f"[CẢNH BÁO]: Không tìm thấy thư mục adapter tại: {lora_dir}")
    print("Mô hình sẽ chỉ có thể chạy ở chế độ Base Model.")

# Nạp Model
print("Đang nạp mô hình Qwen2.5-Coder-1.5B (4-bit QLoRA)...")
if has_cuda:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
else:
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

if os.path.exists(lora_dir):
    tokenizer = AutoTokenizer.from_pretrained(lora_dir)
    model = PeftModel.from_pretrained(base_model, lora_dir)
    has_adapter = True
else:
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    model = base_model
    has_adapter = False

model.eval()
print("-> Đã nạp mô hình thành công vào bộ nhớ!\n")

def generate_text(prompt, use_adapter=True):
    inputs = tokenizer(prompt, return_tensors="pt")
    if has_cuda:
        inputs = inputs.to("cuda")

    start_time = time.time()
    with torch.no_grad():
        if has_adapter and not use_adapter:
            with model.disable_adapter():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1
                )
        else:
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )
    elapsed = time.time() - start_time
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
    return response, round(elapsed, 2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Management System - Codebase AI Copilot</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Marked.js for Markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Highlight.js for Code -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        pre code { border-radius: 0.5rem; font-size: 0.875rem; }
        .prose pre { padding: 0.75rem; background: #0f172a; margin: 0.5rem 0; overflow-x: auto; }
        .prose code { background: #1e293b; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.85em; }
        .prose p { margin-bottom: 0.5rem; }
        .prose ul, .prose ol { margin-left: 1.25rem; margin-bottom: 0.5rem; list-style-type: disc; }
        .scroll-smooth { scroll-behavior: smooth; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">

    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center font-bold text-xl shadow-lg shadow-cyan-500/20">
                ⚡
            </div>
            <div>
                <h1 class="font-bold text-lg text-white flex items-center gap-2">
                    Course Management System <span class="text-xs px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">AI Copilot</span>
                </h1>
                <p class="text-xs text-slate-400">So sánh đối chứng trực tiếp: <span class="text-slate-300 font-semibold">Base Model (Chưa train)</span> vs <span class="text-emerald-400 font-semibold">Fine-tuned (QLoRA)</span></p>
            </div>
        </div>

        <!-- Mode Selector -->
        <div class="flex items-center bg-slate-800 p-1 rounded-xl border border-slate-700">
            <button onclick="setMode('compare')" id="btn-compare" class="px-3 py-1.5 rounded-lg text-xs font-medium transition bg-cyan-600 text-white shadow">
                ⚡ So sánh Song song (A/B)
            </button>
            <button onclick="setMode('finetuned')" id="btn-finetuned" class="px-3 py-1.5 rounded-lg text-xs font-medium transition text-slate-300 hover:text-white">
                🚀 Chỉ Fine-tuned
            </button>
            <button onclick="setMode('base')" id="btn-base" class="px-3 py-1.5 rounded-lg text-xs font-medium transition text-slate-300 hover:text-white">
                🌐 Chỉ Base Model
            </button>
        </div>

        <!-- Hardware Badge -->
        <div class="text-xs flex items-center gap-2 text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>GPU: {{ gpu_name }} (4-bit QLoRA)</span>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 flex flex-col">

        <!-- Quick Prompts (Gợi ý câu hỏi nhanh) -->
        <div class="mb-4">
            <p class="text-xs text-slate-400 mb-2 font-medium">💡 Gợi ý câu hỏi thử nghiệm để thấy rõ sự khác biệt:</p>
            <div class="flex flex-wrap gap-2">
                <button onclick="sendQuickPrompt('Lớp SearchCriteria trong package specification giữ vai trò gì và gồm những trường nào?')" 
                        class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-slate-700/70 transition">
                    📌 Hỏi về SearchCriteria
                </button>
                <button onclick="sendQuickPrompt('Viết cấu trúc lớp CategoryDaoImpl kế thừa HibernatePaginationSortingDao theo chuẩn của dự án.')" 
                        class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-slate-700/70 transition">
                    💻 Sinh code DAO mới
                </button>
                <button onclick="sendQuickPrompt('Giải thích cơ chế nâng version khi người dùng upload tài liệu trùng tên trong DocumentServiceImpl.')" 
                        class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-slate-700/70 transition">
                    📂 Nghiệp vụ Versioning tài liệu
                </button>
                <button onclick="sendQuickPrompt('Dự án Course Management System gồm những module và package chính nào?')" 
                        class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg border border-slate-700/70 transition">
                    🏗️ Cấu trúc Package dự án
                </button>
            </div>
        </div>

        <!-- Chat Messages Container -->
        <div id="chat-box" class="flex-1 overflow-y-auto space-y-6 pb-6">
            <!-- Tin nhắn mẫu chào mừng -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-6 text-sm text-slate-300 leading-relaxed shadow-lg">
                <h3 class="text-base font-semibold text-white mb-2 flex items-center gap-2">
                    👋 Chào mừng bạn đến với Bộ điều khiển AI Chatbot của dự án!
                </h3>
                <p>Hệ thống cho phép bạn gửi câu hỏi và nhận câu trả lời phân luồng từ hai nguồn:</p>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                    <div class="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">🌐 Base Model (Chưa train)</span>
                        <p class="text-xs text-slate-400">Mô hình Qwen2.5-Coder gốc, chỉ có kiến thức lập trình tổng quát ngoài Internet, chưa biết cấu trúc dự án của bạn.</p>
                    </div>
                    <div class="bg-slate-950/60 p-3 rounded-xl border border-emerald-900/50">
                        <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block mb-1">🚀 Fine-tuned Model (Đã train)</span>
                        <p class="text-xs text-slate-400">Đã nạp LoRA Adapter, am hiểu 100% kiến trúc Generic DAO, các Entity, MinIO Storage và quy tắc nghiệp vụ dự án.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Input Box -->
        <div class="mt-auto pt-3 border-t border-slate-800 sticky bottom-0 bg-slate-950">
            <form id="chat-form" onsubmit="handleSend(event)" class="relative flex items-center">
                <textarea id="user-input" rows="1" placeholder="Nhập câu hỏi về dự án Course Management System... (Shift+Enter để xuống dòng)"
                          class="w-full bg-slate-900 text-slate-100 placeholder-slate-500 rounded-xl pl-4 pr-24 py-3.5 border border-slate-800 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-sm resize-none"
                          onkeydown="handleKeyDown(event)"></textarea>
                <button type="submit" id="send-btn"
                        class="absolute right-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white rounded-lg text-sm font-medium transition shadow-md flex items-center gap-1.5 disabled:opacity-50">
                    <span>Gửi</span>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                </button>
            </form>
            <div class="flex justify-between items-center text-[11px] text-slate-500 px-1 mt-1.5">
                <span>Nhấn <strong>Enter</strong> để gửi, <strong>Shift + Enter</strong> để xuống dòng.</span>
                <button onclick="clearChat()" class="hover:text-slate-400 transition underline">Xóa lịch sử chat</button>
            </div>
        </div>

    </main>

    <script>
        let currentMode = 'compare';

        function setMode(mode) {
            currentMode = mode;
            ['compare', 'finetuned', 'base'].forEach(m => {
                const btn = document.getElementById(`btn-${m}`);
                if (m === mode) {
                    btn.className = "px-3 py-1.5 rounded-lg text-xs font-medium transition bg-cyan-600 text-white shadow";
                } else {
                    btn.className = "px-3 py-1.5 rounded-lg text-xs font-medium transition text-slate-300 hover:text-white";
                }
            });
        }

        function handleKeyDown(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend(e);
            }
        }

        function sendQuickPrompt(text) {
            document.getElementById('user-input').value = text;
            handleSend(new Event('submit'));
        }

        function clearChat() {
            document.getElementById('chat-box').innerHTML = `
                <div class="text-center text-xs text-slate-500 py-6">Đã làm mới cuộc hội thoại. Hãy bắt đầu hỏi một câu mới!</div>
            `;
        }

        async function handleSend(e) {
            if (e) e.preventDefault();
            const inputEl = document.getElementById('user-input');
            const query = inputEl.value.trim();
            if (!query) return;

            inputEl.value = '';
            const sendBtn = document.getElementById('send-btn');
            sendBtn.disabled = true;

            const chatBox = document.getElementById('chat-box');

            // Render tin nhắn của User
            const userMsgHtml = `
                <div class="flex justify-end mb-4">
                    <div class="bg-indigo-600 text-white text-sm px-4 py-3 rounded-2xl rounded-tr-none max-w-2xl shadow-md">
                        <strong>Bạn:</strong> ${escapeHtml(query)}
                    </div>
                </div>
            `;
            chatBox.insertAdjacentHTML('beforeend', userMsgHtml);

            // Render khung phản hồi đang tải (Loading card)
            const loadingId = 'loading-' + Date.now();
            let loadingHtml = '';

            if (currentMode === 'compare') {
                loadingHtml = `
                    <div id="${loadingId}" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl animate-pulse">
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-slate-400">🌐 BASE MODEL (Chưa train)</span>
                                <span class="text-xs text-slate-500">Đang sinh câu trả lời...</span>
                            </div>
                            <div class="h-4 bg-slate-800 rounded w-3/4 mb-2"></div>
                            <div class="h-4 bg-slate-800 rounded w-1/2"></div>
                        </div>
                        <div class="bg-slate-900 border border-emerald-900/50 p-4 rounded-2xl animate-pulse">
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-xs font-bold text-emerald-400">🚀 FINE-TUNED MODEL (QLoRA)</span>
                                <span class="text-xs text-emerald-500">Đang suy nghĩ kiến trúc...</span>
                            </div>
                            <div class="h-4 bg-slate-800 rounded w-4/5 mb-2"></div>
                            <div class="h-4 bg-slate-800 rounded w-2/3"></div>
                        </div>
                    </div>
                `;
            } else {
                const title = currentMode === 'finetuned' ? '🚀 FINE-TUNED MODEL' : '🌐 BASE MODEL';
                const borderColor = currentMode === 'finetuned' ? 'border-emerald-900/50' : 'border-slate-800';
                loadingHtml = `
                    <div id="${loadingId}" class="bg-slate-900 border ${borderColor} p-4 rounded-2xl mb-4 animate-pulse">
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-xs font-bold text-cyan-400">${title}</span>
                            <span class="text-xs text-slate-500">Đang sinh câu trả lời...</span>
                        </div>
                        <div class="h-4 bg-slate-800 rounded w-3/4 mb-2"></div>
                        <div class="h-4 bg-slate-800 rounded w-1/2"></div>
                    </div>
                `;
            }

            chatBox.insertAdjacentHTML('beforeend', loadingHtml);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: query, mode: currentMode })
                });
                const data = await res.json();
                document.getElementById(loadingId).remove();

                if (currentMode === 'compare') {
                    const baseMarkdown = marked.parse(data.base || 'Không có phản hồi');
                    const ftMarkdown = marked.parse(data.finetuned || 'Không có phản hồi');

                    const responseHtml = `
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <!-- Cột Base Model -->
                            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col shadow-lg">
                                <div class="flex items-center justify-between pb-3 mb-3 border-b border-slate-800 text-xs">
                                    <div class="flex items-center gap-2">
                                        <span class="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                                        <span class="font-bold text-slate-300">Base Model (Chưa train)</span>
                                    </div>
                                    <span class="text-slate-500 font-mono">${data.time_base}s</span>
                                </div>
                                <div class="prose text-xs text-slate-300 leading-relaxed overflow-x-auto flex-1">
                                    ${baseMarkdown}
                                </div>
                            </div>

                            <!-- Cột Fine-tuned Model -->
                            <div class="bg-slate-900 border border-emerald-500/40 rounded-2xl p-4 sm:p-5 flex flex-col shadow-lg shadow-emerald-950/20">
                                <div class="flex items-center justify-between pb-3 mb-3 border-b border-emerald-900/40 text-xs">
                                    <div class="flex items-center gap-2">
                                        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                                        <span class="font-bold text-emerald-400">Fine-tuned Model (QLoRA)</span>
                                        <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-mono">Am hiểu Codebase</span>
                                    </div>
                                    <span class="text-emerald-500 font-mono">${data.time_finetuned}s</span>
                                </div>
                                <div class="prose text-xs text-slate-200 leading-relaxed overflow-x-auto flex-1">
                                    ${ftMarkdown}
                                </div>
                            </div>
                        </div>
                    `;
                    chatBox.insertAdjacentHTML('beforeend', responseHtml);
                } else if (currentMode === 'finetuned') {
                    const ftMarkdown = marked.parse(data.finetuned || '');
                    const responseHtml = `
                        <div class="bg-slate-900 border border-emerald-500/40 rounded-2xl p-5 mb-6 shadow-lg">
                            <div class="flex items-center justify-between pb-3 mb-3 border-b border-emerald-900/40 text-xs">
                                <span class="font-bold text-emerald-400 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> Fine-tuned Model (QLoRA)
                                </span>
                                <span class="text-emerald-500 font-mono">${data.time_finetuned}s</span>
                            </div>
                            <div class="prose text-sm text-slate-200 leading-relaxed">
                                ${ftMarkdown}
                            </div>
                        </div>
                    `;
                    chatBox.insertAdjacentHTML('beforeend', responseHtml);
                } else {
                    const baseMarkdown = marked.parse(data.base || '');
                    const responseHtml = `
                        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-6 shadow-lg">
                            <div class="flex items-center justify-between pb-3 mb-3 border-b border-slate-800 text-xs">
                                <span class="font-bold text-slate-300 flex items-center gap-2">
                                    <span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span> Base Model (Chưa train)
                                </span>
                                <span class="text-slate-500 font-mono">${data.time_base}s</span>
                            </div>
                            <div class="prose text-sm text-slate-300 leading-relaxed">
                                ${baseMarkdown}
                            </div>
                        </div>
                    `;
                    chatBox.insertAdjacentHTML('beforeend', responseHtml);
                }

                // Highlight code blocks
                document.querySelectorAll('pre code').forEach((el) => {
                    hljs.highlightElement(el);
                });

            } catch (err) {
                console.error(err);
                if (document.getElementById(loadingId)) {
                    document.getElementById(loadingId).remove();
                }
                chatBox.insertAdjacentHTML('beforeend', `
                    <div class="bg-red-950/60 border border-red-800 text-red-200 text-xs p-4 rounded-xl mb-4">
                        <strong>Lỗi:</strong> Không thể kết nối với server sinh câu trả lời: ${err.message}
                    </div>
                `);
            } finally {
                sendBtn.disabled = false;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        function escapeHtml(text) {
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, gpu_name=gpu_name)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    mode = data.get("mode", "compare")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    system_prompt = "Bạn là trợ lý AI chuyên gia, nắm vững 100% kiến trúc, mã nguồn và nghiệp vụ của dự án Course Management System (Hệ thống Quản lý Khóa học, Học viên & Tài liệu MinIO)."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    result = {}

    if mode == "compare":
        # Sinh câu trả lời từ Base Model (Tắt adapter)
        base_resp, base_time = generate_text(prompt, use_adapter=False)
        result["base"] = base_resp
        result["time_base"] = base_time

        # Sinh câu trả lời từ Fine-tuned Model (Bật adapter)
        ft_resp, ft_time = generate_text(prompt, use_adapter=True)
        result["finetuned"] = ft_resp
        result["time_finetuned"] = ft_time

    elif mode == "finetuned":
        ft_resp, ft_time = generate_text(prompt, use_adapter=True)
        result["finetuned"] = ft_resp
        result["time_finetuned"] = ft_time

    elif mode == "base":
        base_resp, base_time = generate_text(prompt, use_adapter=False)
        result["base"] = base_resp
        result["time_base"] = base_time

    return jsonify(result)

if __name__ == "__main__":
    port = 7860
    print(f"\n=======================================================")
    print(f"WEB CHATBOT ĐÃ SẴN SÀNG TẠI: http://localhost:{port}")
    print(f"Mở trình duyệt web của bạn và truy cập link trên!")
    print(f"=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)
