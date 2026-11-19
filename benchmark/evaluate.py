"""Run a controlled local LoRA/RAG ablation and optional OpenRouter baselines."""

import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from evaluation_core import build_messages, paired_comparison, summarize, validate_reviews

ROOT = Path(__file__).resolve().parents[1]
CHATBOT = ROOT / "chatbot"
sys.path.insert(0, str(CHATBOT))
from rag_engine import CodebaseRAG

LOCAL_VARIANTS = {
    "base": (False, False), "base_rag": (False, True),
    "lora": (True, False), "lora_rag": (True, True),
}
CLOUD_VARIANTS = {"cloud_zero": False, "cloud_rag": True}
DEFAULT_MODES = list(LOCAL_VARIANTS)
ADAPTER = ROOT / "outputs" / "course-management-lora-adapter"


class LocalConfigurationError(RuntimeError):
    pass


def _console_message(message, stream=None, flush=False):
    """Do not fail a completed run when a Windows console cannot encode a path."""
    stream = stream or sys.stdout
    encoding = getattr(stream, "encoding", None)
    if encoding:
        message = str(message).encode(encoding, errors="backslashreplace").decode(encoding)
    print(message, file=stream, flush=flush)


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def load_cases(path):
    cases = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not all(item.get(key) for key in ("id", "category", "kind", "question", "checks", "sources")):
            raise ValueError(f"Invalid case at line {line_number}")
        if item["kind"] not in ("qa", "code") or not isinstance(item["checks"], list):
            raise ValueError(f"Invalid case type/checks at line {line_number}")
        for source in item["sources"]:
            source_path = (ROOT / source).resolve()
            if not source_path.is_relative_to(ROOT) or not source_path.is_file():
                raise ValueError(f"Missing or invalid source for {item['id']}: {source}")
        cases.append(item)
    if not cases or len({item["id"] for item in cases}) != len(cases):
        raise ValueError("Empty cases or duplicate IDs")
    return cases


def select_cases(cases, categories=None, case_ids=None, limit=0):
    """Select a reproducible subset without silently ignoring unknown selectors."""
    categories, case_ids = set(categories or []), set(case_ids or [])
    if categories - {case["category"] for case in cases}:
        raise ValueError("Unknown benchmark category")
    if case_ids - {case["id"] for case in cases}:
        raise ValueError("Unknown benchmark case ID")
    if limit < 0:
        raise ValueError("limit must be non-negative")
    selected = [case for case in cases if (not categories or case["category"] in categories)
                and (not case_ids or case["id"] in case_ids)]
    if not selected:
        raise ValueError("No benchmark cases match the selectors")
    return selected[:limit] if limit else selected


def read_api_key():
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"].strip()
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip("\"").strip("'")
    return ""


class LocalModel:
    def __init__(self, max_tokens):
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        self.torch = torch
        self.max_tokens = max_tokens
        if not torch.cuda.is_available() and os.environ.get("LOCAL_ALLOW_CPU", "false").lower() not in ("1", "true", "yes"):
            raise LocalConfigurationError("CUDA unavailable; set LOCAL_ALLOW_CPU=true to explicitly permit high-RAM CPU inference")
        config = json.loads((ADAPTER / "adapter_config.json").read_text(encoding="utf-8"))
        model_id = config["base_model_name_or_path"]
        local = os.environ.get("LOCAL_MODEL_PATH", r"D:\models\Qwen2.5-Coder-3B-Instruct-sharded")
        self.model_source = local if Path(local).is_dir() else model_id
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(str(ADAPTER), local_files_only=True)
        if torch.cuda.is_available():
            quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                               bnb_4bit_compute_dtype=torch.float16,
                                               bnb_4bit_use_double_quant=True)
            base = AutoModelForCausalLM.from_pretrained(self.model_source, quantization_config=quantization,
                                                        device_map="auto", local_files_only=True)
            self.device = "cuda"
        else:
            base = AutoModelForCausalLM.from_pretrained(self.model_source, torch_dtype=torch.float32,
                                                        device_map="cpu", local_files_only=True)
            self.device = "cpu"
        self.model = PeftModel.from_pretrained(base, str(ADAPTER), local_files_only=True)
        self.model.eval()

    def generate(self, messages, use_adapter):
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        if self.device == "cuda":
            self.torch.cuda.synchronize()
            self.torch.cuda.reset_peak_memory_stats()
        start = time.perf_counter()
        adapter_context = contextlib.nullcontext() if use_adapter else self.model.disable_adapter()
        with adapter_context, self.torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=self.max_tokens, do_sample=False,
                                         repetition_penalty=1.0, pad_token_id=self.tokenizer.eos_token_id)
        if self.device == "cuda":
            self.torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        generated = output[0][inputs.input_ids.shape[1]:]
        return {"answer": self.tokenizer.decode(generated, skip_special_tokens=True).strip(),
                "elapsed_seconds": round(elapsed, 3), "output_tokens": len(generated),
                "input_tokens": int(inputs.input_ids.shape[1]),
                "possibly_truncated": len(generated) >= self.max_tokens and int(generated[-1]) != self.tokenizer.eos_token_id,
                "peak_gpu_allocated_mib": round(self.torch.cuda.max_memory_allocated() / 1024**2, 1)
                if self.device == "cuda" else None}


def cloud_generate(messages, model, key, max_tokens):
    import requests
    started = time.perf_counter()
    if not key:
        return {"status": "error", "error": "missing_openrouter_key", "elapsed_seconds": 0.0}
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers={"Authorization": f"Bearer {key}"},
                                 json={"model": model, "messages": messages, "temperature": 0,
                                       "max_tokens": max_tokens, "stream": False}, timeout=(10, 90))
        elapsed = round(time.perf_counter() - started, 3)
        if response.status_code != 200:
            return {"status": "error", "error": f"http_{response.status_code}", "elapsed_seconds": elapsed}
        payload = response.json()
        choices = payload.get("choices") or []
        returned_model = payload.get("model")
        if returned_model != model:
            return {"status": "error", "error": "unexpected_or_missing_model_id", "elapsed_seconds": elapsed,
                    "returned_model": returned_model}
        answer = ((choices[0].get("message") or {}).get("content") or "").strip() if choices else ""
        if not answer:
            return {"status": "error", "error": "empty_response", "elapsed_seconds": elapsed,
                    "returned_model": payload.get("model"), "usage": payload.get("usage"),
                    "finish_reason": choices[0].get("finish_reason") if choices else None}
        return {"status": "ok", "answer": answer, "elapsed_seconds": elapsed,
                "returned_model": payload.get("model"), "usage": payload.get("usage"),
                "finish_reason": choices[0].get("finish_reason")}
    except (requests.RequestException, ValueError, TypeError, AttributeError):
        return {"status": "error", "error": "network_or_invalid_response",
                "elapsed_seconds": round(time.perf_counter() - started, 3)}


def make_report(run_dir):
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (run_dir / "results.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    reviews = [json.loads(line) for line in (run_dir / "reviews.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    validated = validate_reviews(records, reviews)
    summary = summarize(records, validated)
    lines = ["# Báo cáo đánh giá AI", "", f"Run: `{manifest['run_id']}`  ",
             f"Bộ câu hỏi SHA-256: `{manifest['cases_sha256']}`", "",
             "Các câu chưa được đánh giá thủ công không tính vào tỷ lệ đạt; lỗi API/mô hình được báo riêng.",
             "Kết quả chấm tay, bao gồm compile/test, là khai báo của người chấm và cần được đối chiếu với bằng chứng.", "",
             "| Cấu hình | Lượt | Lỗi | Đã chấm | Chờ chấm | Đạt/đã chấm | Compile đạt/đã kiểm tra | Test đạt/đã kiểm tra | TG TB thành công (s) |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for variant, value in summary.items():
        rate = "N/A" if value["pass_rate_percent"] is None else f"{value['passed']}/{value['reviewed']}" + (f" ({value['pass_rate_percent']}%)" if value["reviewed"] >= 5 else " (ít mẫu)")
        elapsed = value["mean_seconds_successful"] if value["mean_seconds_successful"] is not None else "N/A"
        lines.append(f"| {variant} | {value['attempts']} | {value['errors']} | {value['reviewed']} | {value['pending']} | {rate} | {value['compile_passed']}/{value['compile_checked']} | {value['tests_passed']}/{value['tests_checked']} | {elapsed} |")
    lines.extend(["", "## Theo nhóm tình huống", "",
                  "| Nhóm | Cấu hình | Số đã chấm | Đạt/đã chấm | Lỗi |",
                  "|---|---|---:|---:|---:|"])
    for category in sorted({row["category"] for row in records}):
        grouped = summarize([row for row in records if row["category"] == category], validated)
        for variant, value in grouped.items():
            rate = "N/A" if not value["reviewed"] else f"{value['passed']}/{value['reviewed']}" + (f" ({value['pass_rate_percent']}%)" if value["reviewed"] >= 5 else " (ít mẫu)")
            lines.append(f"| {category} | {variant} | {value['reviewed']} | {rate} | {value['errors']} |")
    lines.extend(["", "Chênh lệch chỉ tính các cặp cùng câu hỏi/lần chạy đã được chấm ở cả hai phía.", ""])
    for left, right in (("base", "base_rag"), ("base", "lora"), ("base_rag", "lora_rag"),
                        ("lora", "lora_rag"), ("cloud_zero", "cloud_rag")):
        if left in summary and right in summary:
            pair = paired_comparison(records, validated, left, right)
            diff = pair["difference_percentage_points"]
            lines.append(f"- {left} → {right}: {pair['paired_reviewed']} cặp đã chấm; " +
                         ("chưa hiển thị chênh lệch vì có dưới 5 cặp." if pair["paired_reviewed"] < 5
                          else f"chênh lệch {diff:+.1f} điểm phần trăm."))
    lines.extend(["", "## Phạm vi", "", "Bộ câu hỏi pilot có thể trùng kiến thức dữ liệu huấn luyện; không coi là tập hold-out độc lập.",
                  "So sánh Cloud zero-context phản ánh việc thiếu thông tin, không phải giới hạn cố hữu của model.",
                  "Thời gian Cloud bao gồm mạng; thời gian local là sinh sau khi nạp model. Không dùng làm kết luận nhân quả khi chưa đủ mẫu và đối chứng.",
                  "Ngưỡng 5 cặp chỉ là ngưỡng hiển thị; đạt ngưỡng không có nghĩa là đủ bằng chứng thống kê.", ""])
    (run_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def run(args):
    cases_path = args.cases.resolve()
    cases = select_cases(load_cases(cases_path), categories=getattr(args, "category", None),
                         case_ids=getattr(args, "case_id", None), limit=args.limit)
    if args.repeats < 1 or args.max_tokens < 1:
        raise ValueError("repeats and max-tokens must be positive")
    modes = args.modes.split(",")
    allowed = set(LOCAL_VARIANTS) | set(CLOUD_VARIANTS)
    if len(set(modes)) != len(modes) or not modes or any(mode not in allowed for mode in modes):
        raise ValueError("Invalid or repeated mode")
    if any(mode in CLOUD_VARIANTS for mode in modes):
        if not args.openrouter_model or not args.openrouter_model.endswith(":free"):
            raise ValueError("Cloud requires an explicit :free OpenRouter model ID; random Free Router is not allowed")

    rag = CodebaseRAG(str(ROOT))
    corpus = "\n".join(f"{doc['path']}\0{digest(doc['content'])}" for doc in sorted(rag.docs, key=lambda item: item["path"]))
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run_dir = (args.output_dir / run_id).resolve()
    run_dir.mkdir(parents=True, exist_ok=False)
    local = None
    init_error = None
    load_started = time.perf_counter()
    if any(mode in LOCAL_VARIANTS for mode in modes):
        try:
            local = LocalModel(args.max_tokens)
        except Exception as exc:
            init_error = type(exc).__name__
            detail = f": {exc}" if isinstance(exc, LocalConfigurationError) else ""
            _console_message(f"Không thể nạp model local: {init_error}{detail}", stream=sys.stderr)
    load_seconds = round(time.perf_counter() - load_started, 3) if any(mode in LOCAL_VARIANTS for mode in modes) else None
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        git_dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError):
        git_commit, git_dirty = None, None
    package_versions = {}
    for package in ("torch", "transformers", "peft", "accelerate", "bitsandbytes", "requests"):
        try:
            package_versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            package_versions[package] = None
    manifest = {"run_id": run_id, "created_utc": datetime.now(timezone.utc).isoformat(),
                "cases_sha256": file_digest(cases_path), "selected_cases_sha256": digest(json.dumps(cases, ensure_ascii=False, sort_keys=True)),
                "case_count": len(cases), "modes": modes,
                "repeats": args.repeats, "corpus_sha256": digest(corpus), "rag_top_k": 3, "rag_max_chars": 1800,
                "python": platform.python_version(), "platform": platform.platform(), "max_new_tokens": args.max_tokens,
                "git_commit": git_commit, "git_dirty": git_dirty, "local_load_seconds": load_seconds,
                "package_versions": package_versions,
                "decoding": "greedy local; cloud temperature=0 (provider behavior may vary)",
                "local_model_id": local.model_id if local else None,
                "local_model_source": local.model_source if local else None,
                "local_device": local.device if local else None,
                "torch_version": str(local.torch.__version__) if local else None,
                "cuda_version": local.torch.version.cuda if local else None,
                "gpu_name": local.torch.cuda.get_device_name(0) if local and local.device == "cuda" else None,
                "adapter_sha256": file_digest(ADAPTER / "adapter_model.safetensors") if local else None,
                "local_initialization_error": init_error, "cloud_model_requested": args.openrouter_model,
                "note": "Pilot suite: no verified hold-out; generated code is not compiled or executed automatically."}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    key = read_api_key() if any(mode in CLOUD_VARIANTS for mode in modes) else ""
    rows, reviews = [], []
    with (run_dir / "results.jsonl").open("w", encoding="utf-8") as output, \
         (run_dir / "contexts.jsonl").open("w", encoding="utf-8") as contexts:
        for case in cases:
            context, files = rag.format_context_block(case["question"], top_k=3, max_chars=1800)
            contexts.write(json.dumps({"case_id": case["id"], "context": context, "rag_files": files,
                                       "context_sha256": digest(context)}, ensure_ascii=False) + "\n")
            contexts.flush()
            for repeat in range(args.repeats):
                for mode in modes:
                    use_rag = LOCAL_VARIANTS[mode][1] if mode in LOCAL_VARIANTS else CLOUD_VARIANTS[mode]
                    messages = build_messages(case["question"], context if use_rag else "")
                    row = {"id": f"{case['id']}/{mode}/{repeat}", "case_id": case["id"], "variant": mode,
                           "repeat": repeat, "category": case["category"], "kind": case["kind"],
                           "prompt_sha256": digest(json.dumps(messages, ensure_ascii=False)),
                           "context_sha256": digest(context) if use_rag else None,
                           "rag_files": files if use_rag else [], "status": "error", "answer": ""}
                    _console_message(f"{row['id']}...", flush=True)
                    if mode in LOCAL_VARIANTS:
                        if local is None:
                            row.update(error=f"local_initialization_{init_error}", elapsed_seconds=0.0)
                        else:
                            started = time.perf_counter()
                            try:
                                row.update(local.generate(messages, LOCAL_VARIANTS[mode][0]))
                                row["status"] = "ok" if row["answer"] else "error"
                                if not row["answer"]:
                                    row["error"] = "empty_response"
                            except Exception as exc:
                                row.update(error=type(exc).__name__, elapsed_seconds=round(time.perf_counter() - started, 3))
                    else:
                        row.update(cloud_generate(messages, args.openrouter_model, key, args.max_tokens))
                    output.write(json.dumps(row, ensure_ascii=False) + "\n")
                    output.flush()
                    rows.append(row)
                    reviews.append({"id": row["id"], "verdict": "pending", "reviewer": "", "evidence": "",
                                    "compile_status": "not_run", "test_status": "not_run"})
    (run_dir / "reviews.jsonl").write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in reviews), encoding="utf-8")
    make_report(run_dir)
    _console_message(f"Kết quả: {run_dir}")
    if not any(row["status"] == "ok" for row in rows):
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    execute = sub.add_parser("run", help="Generate responses and an unreviewed report")
    execute.add_argument("--cases", type=Path, default=ROOT / "benchmark" / "cases.jsonl")
    execute.add_argument("--output-dir", type=Path, default=ROOT / "benchmark" / "runs")
    execute.add_argument("--modes", default=",".join(DEFAULT_MODES))
    execute.add_argument("--openrouter-model", default=None)
    execute.add_argument("--limit", type=int, default=0, help="0 means all cases")
    execute.add_argument("--category", action="append", help="Select a category; repeat to include multiple categories")
    execute.add_argument("--case-id", action="append", help="Select a case ID; repeat to include multiple cases")
    execute.add_argument("--repeats", type=int, default=1)
    execute.add_argument("--max-tokens", type=int, default=512)
    report = sub.add_parser("report", help="Recalculate a report after reviewing responses")
    report.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    if args.command == "report":
        make_report(args.run_dir)
        _console_message(f"Đã cập nhật {args.run_dir / 'report.md'}")
        return 0
    if args.limit < 0 or args.repeats < 1 or args.max_tokens < 1:
        parser.error("limit must be >= 0; repeats and max-tokens must be >= 1")
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
