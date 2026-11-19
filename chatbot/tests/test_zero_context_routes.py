import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import ANY, MagicMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["HF_HUB_OFFLINE"] = "1"

with patch("threading.Thread.start"), patch("transformers.AutoTokenizer.from_pretrained"):
    import web_app
    web_app._load_local_libraries()


class ZeroContextRoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = web_app.app.test_client()

    def test_ui_displays_model_picker(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'particle-ai/particle-1:free', response.data)
        self.assertIn(b'btn-zero_context', response.data)
        self.assertNotIn("cột fine-tuned dùng Base và tắt LoRA".encode(), response.data)
        self.assertNotIn("3 AI cùng sinh mã nguồn song song".encode(), response.data)

    def test_legacy_keyword_evaluation_is_marked_unverified(self):
        response = self.client.post("/api/score_response", json={
            "prompt": "Giải thích lưu tài liệu ở đâu?", "text": "File và metadata đều ở MinIO."})
        self.assertFalse(response.get_json()["quality_verified"])
        self.assertEqual(response.get_json()["evaluation_kind"], "keyword_heuristic_unverified")

    def test_latest_benchmark_report_is_displayed_as_escaped_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "benchmark/runs/run-1/report.md"
            report.parent.mkdir(parents=True)
            report.write_text("# Review\n<script>alert(1)</script>", encoding="utf-8")
            with patch.object(web_app, "root_dir", tmp):
                response = self.client.get("/benchmark-report")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"&lt;script&gt;", response.data)
            self.assertNotIn(b"<script>alert(1)</script>", response.data)

    def test_report_renders_structured_results_without_html_injection(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "benchmark/runs/20260101T000000.000000Z"
            run.mkdir(parents=True)
            (run / "manifest.json").write_text(json.dumps({"case_count": 1}), encoding="utf-8")
            (run / "cases.json").write_text(json.dumps([{"id": "case-1", "question": "<script>alert(1)</script>"}]), encoding="utf-8")
            result = {"id": "case-1/base/0", "case_id": "case-1", "variant": "base", "repeat": 0,
                      "status": "ok", "kind": "qa", "answer": "<img src=x>", "elapsed_seconds": 1}
            (run / "results.jsonl").write_text(json.dumps(result) + "\n", encoding="utf-8")
            with patch.object(web_app, "root_dir", tmp):
                response = self.client.get("/benchmark-report")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"&lt;script&gt;", response.data)
            self.assertIn(b"&lt;img src=x&gt;", response.data)
            self.assertNotIn(b"<script>alert(1)</script>", response.data)
            self.assertIn("Chưa chấm".encode(), response.data)

    def test_stream_does_not_retrieve_rag_or_forward_history(self):
        with patch.object(web_app, "retrieve_rag_for_query") as rag, \
             patch.object(web_app, "stream_zero_context", return_value=iter(["answer"])) as stream, \
             patch.object(web_app, "openrouter_api_key", "test-key"):
            response = self.client.post("/api/chat_stream", json={
                "message": "question", "mode": "zero_context",
                "history": [{"role": "user", "content": "private old context"}],
                "zero_model": "recursive/flint-v1.0:free",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"answer", response.data)
            self.assertNotIn(b"private old context", response.data)
            rag.assert_not_called()
            stream.assert_called_once_with("question", "recursive/flint-v1.0:free", "test-key", generation_info=ANY)

    def test_live_review_uses_local_base_and_validates_judgement(self):
        with patch.object(web_app, "local_ready", True), patch.object(web_app, "model", Mock()), \
             patch.object(web_app, "generate_local", return_value=(
                 '{"score": 72, "feedback": "Trả lời đúng trọng tâm nhưng còn thiếu ví dụ."}', 1.1)) as generate:
            response = self.client.post("/api/evaluate_response", json={"question": "Java là gì?", "answer": "Một ngôn ngữ lập trình."})
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(result["score"], 72)
        self.assertIn("thiếu", result["feedback"])
        self.assertFalse(result["quality_verified"])
        self.assertFalse(generate.call_args.kwargs["use_adapter"])
        self.assertFalse(generate.call_args.kwargs["use_rag"])

    def test_live_review_rejects_invalid_or_empty_input_and_invalid_ai_output(self):
        self.assertEqual(self.client.post("/api/evaluate_response", json={"question": "", "answer": "x"}).status_code, 400)
        self.assertEqual(self.client.post("/api/evaluate_response", json={"question": "x", "answer": "a" * 12001}).status_code, 400)
        with patch.object(web_app, "local_ready", True), patch.object(web_app, "model", Mock()), \
             patch.object(web_app, "generate_local", return_value=('{"score": 300, "feedback": "fine"}', 1)):
            self.assertEqual(self.client.post("/api/evaluate_response", json={"question": "q", "answer": "a"}).status_code, 502)

    def test_live_review_reports_unavailable_local_model(self):
        with patch.object(web_app, "local_ready", False), patch.object(web_app, "ensure_local_model", return_value=False), patch.object(web_app, "generate_local") as generate:
            response = self.client.post("/api/evaluate_response", json={"question": "q", "answer": "a"})
            self.assertEqual(response.status_code, 503)
            generate.assert_not_called()

    def test_rejects_unknown_and_non_string_models(self):
        for model in ("paid/model", []):
            response = self.client.post("/api/chat_stream", json={
                "message": "question", "mode": "zero_context", "zero_model": model,
            })
            self.assertEqual(response.status_code, 400)

    def test_sync_mode_uses_the_same_isolated_request(self):
        with patch.object(web_app, "stream_zero_context", return_value=iter(["answer"])) as stream, \
             patch.object(web_app, "openrouter_api_key", "test-key"):
            response = self.client.post("/api/chat", json={
                "message": "question", "mode": "zero_context",
                "history": [{"role": "user", "content": "secret"}],
                "zero_model": "cohere/north-mini-code:free",
            })
            self.assertEqual(response.get_json()["answer"], "answer")
            stream.assert_called_once_with("question", "cohere/north-mini-code:free", "test-key", generation_info=ANY)

    def test_local_model_load_is_started_only_once_on_demand(self):
        with patch.object(web_app, "local_ready", False), patch.object(web_app, "model", None), \
             patch.object(web_app, "local_load_state", "idle"), patch.object(web_app.threading.Thread, "start") as start:
            self.assertTrue(web_app.start_local_model())
            self.assertTrue(web_app.start_local_model())
            start.assert_called_once()

    def test_cpu_model_loading_requires_explicit_opt_in(self):
        with patch.object(web_app, "local_ready", False), patch.object(web_app, "has_cuda", False), \
             patch.object(web_app, "local_load_state", "loading"), patch.dict(os.environ, {"LOCAL_ALLOW_CPU": "0"}), \
             patch.object(web_app.AutoModelForCausalLM, "from_pretrained") as load:
            web_app.init_local_model()
            load.assert_not_called()
            self.assertEqual(web_app.local_load_state, "error")

    def test_generation_budget_is_not_silently_reduced(self):
        self.assertEqual(web_app._generation_limits("giải thích hàm này", "general", 1500), (1500, 0))
        self.assertEqual(web_app._generation_limits("owo cf all", "clarify", 1500), (1500, 0))

    def test_finish_reason_identifies_token_limit(self):
        import torch
        self.assertEqual(web_app._local_finish_info(torch.tensor([[1, 2, 3, 4]]), 1, 3, 9)["finish_reason"], "length")
        self.assertEqual(web_app._local_finish_info(torch.tensor([[1, 2, 9]]), 1, 3, 9)["finish_reason"], "stop")

    def test_general_prompt_does_not_include_project_instructions_or_rag(self):
        tokenizer = Mock()
        tokenizer.apply_chat_template.return_value = "formatted"
        with patch.object(web_app, "tokenizer", tokenizer), \
             patch.object(web_app, "retrieve_rag_for_query") as rag:
            web_app.format_prompt("Viết một bài thơ về mùa thu", use_rag=True)
            messages = tokenizer.apply_chat_template.call_args.args[0]
            self.assertNotIn("Course Management System", str(messages))
            self.assertNotIn("HibernatePaginationSortingDao", str(messages))
            self.assertNotIn("code Java đầy đủ", str(messages))
            rag.assert_not_called()

    def test_general_prompt_excludes_project_turns_from_history(self):
        tokenizer = Mock()
        tokenizer.apply_chat_template.return_value = "formatted"
        history = [
            {"role": "user", "content": "CourseDaoImpl làm gì?"},
            {"role": "assistant", "content": "CourseDaoImpl là DAO của dự án."},
            {"role": "user", "content": "Thủ đô Việt Nam là gì?"},
            {"role": "assistant", "content": "Hà Nội."},
        ]
        with patch.object(web_app, "tokenizer", tokenizer):
            web_app.format_prompt("Vì sao trời xanh?", use_rag=True, history=history)
            messages = tokenizer.apply_chat_template.call_args.args[0]
            self.assertNotIn("CourseDaoImpl", str(messages))
            self.assertIn("Hà Nội", str(messages))

    def test_arena_ambiguous_input_does_not_retrieve_project_files(self):
        with patch.object(web_app, "retrieve_rag_for_query") as rag, \
             patch.object(web_app, "stream_zero_context", return_value=iter(["baseline"])), \
             patch.object(web_app, "generate_local_stream", return_value=iter(["answer"])):
            response = self.client.post("/api/chat_stream", json={
                "message": "owo cf all", "mode": "compare_arena",
                "zero_model": "recursive/flint-v1.0:free",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'local_direct', response.data)
            rag.assert_not_called()

    def test_general_arena_request_does_not_include_rag(self):
        with patch.object(web_app, "retrieve_rag_for_query") as rag, \
             patch.object(web_app, "stream_zero_context", return_value=iter(["baseline"])), \
             patch.object(web_app, "generate_local_stream", return_value=iter(["answer"])):
            response = self.client.post("/api/chat_stream", json={
                "message": "Viết một bài thơ về mùa thu", "mode": "compare_arena",
                "zero_model": "recursive/flint-v1.0:free",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'local_direct', response.data)
            rag.assert_not_called()

    def test_adapter_selection_is_independent_of_question(self):
        import torch
        from transformers import BatchEncoding
        tokenizer = Mock()
        tokenizer.return_value = BatchEncoding({"input_ids": torch.tensor([[1]])})
        tokenizer.eos_token_id = 2
        tokenizer.decode.return_value = "answer"
        model = MagicMock()
        model.generate.return_value = torch.tensor([[1, 2]])
        with patch.object(web_app, "local_ready", True), patch.object(web_app, "has_cuda", False), \
             patch.object(web_app, "has_adapter", True), patch.object(web_app, "model", model), \
             patch.object(web_app, "tokenizer", tokenizer), patch.object(web_app, "format_prompt", return_value="prompt"):
            web_app.generate_local("Owo là game gì?", use_adapter=True, max_tokens=32)
            model.disable_adapter.assert_not_called()
            web_app.generate_local("owo cf all", use_adapter=False, max_tokens=32)
            model.disable_adapter.assert_called_once()

    def test_rag_control_forces_or_disables_context(self):
        for rag_mode, expected in (("on", True), ("off", False)):
            with self.subTest(rag_mode=rag_mode), \
                 patch.object(web_app, "retrieve_rag_for_query", return_value=("context", ["File.java"])) as rag, \
                 patch.object(web_app, "generate_local_stream", side_effect=lambda *a, **kw: iter(["answer"])) as local:
                response = self.client.post("/api/chat_stream", json={
                    "message": "owo cf all", "mode": "local", "rag_mode": rag_mode, "max_tokens": 512})
                self.assertEqual(response.status_code, 200)
                _ = response.data
                self.assertEqual(rag.called, expected)
                self.assertEqual(local.call_args.kwargs["use_adapter"], True)
                self.assertEqual(local.call_args.kwargs["use_rag"], expected)
                self.assertEqual(local.call_args.kwargs["force_project_context"], expected)
                self.assertEqual(local.call_args.kwargs["max_tokens"], 512)

    def test_arena_calls_both_real_model_options(self):
        calls = []
        def generate(*args, **kwargs):
            calls.append(kwargs["use_adapter"])
            kwargs["generation_info"].update({"finish_reason": "length", "max_new_tokens": 32})
            return iter(["partial"])
        with patch.object(web_app, "stream_zero_context", return_value=iter(["baseline"])), \
             patch.object(web_app, "generate_local_stream", side_effect=generate):
            response = self.client.post("/api/chat_stream", json={"message": "owo cf all", "mode": "compare_arena", "max_tokens": 32})
            _ = response.data
            self.assertEqual(calls, [False, True])
            self.assertIn(b'"finish_reason": "length"', response.data)

    def test_missing_adapter_does_not_silently_run_base(self):
        with patch.object(web_app, "local_ready", True), patch.object(web_app, "has_adapter", False), \
             patch.object(web_app, "model", Mock()) as model:
            info = {}
            result = "".join(web_app.generate_local_stream("owo cf all", generation_info=info))
            self.assertIn("LoRA", result)
            self.assertEqual(info["finish_reason"], "error")
            model.generate.assert_not_called()

    def test_report_rejects_invalid_run_selection(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(web_app, "root_dir", tmp):
            self.assertEqual(self.client.get("/benchmark-report?run=../outside").status_code, 404)
            self.assertIn("Chưa có lần chạy".encode(), self.client.get("/benchmark-report").data)

    def test_project_followup_retrieves_with_previous_project_question(self):
        with patch.object(web_app, "retrieve_rag_for_query", return_value=("project context", ["CourseDaoImpl.java"])) as rag, \
             patch.object(web_app, "generate_local_stream", return_value=iter(["answer"])):
            response = self.client.post("/api/chat_stream", json={
                "message": "giải thích thêm", "mode": "local",
                "history": [{"role": "user", "content": "CourseDaoImpl làm gì?"}],
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'CourseDaoImpl', response.data)
            self.assertIn("CourseDaoImpl", rag.call_args.args[0])

    def test_comparison_uses_selected_baseline_and_no_cloud_substitution(self):
        with patch.object(web_app, "retrieve_rag_for_query", return_value=("context", ["source.java"])), \
             patch.object(web_app, "stream_zero_context", return_value=iter(["baseline"])) as stream, \
             patch.object(web_app, "generate_local_stream", return_value=iter(["local unavailable"])) as local, \
             patch.object(web_app, "call_cloud_gemini_stream") as cloud, \
             patch.object(web_app, "openrouter_api_key", "test-key"):
            response = self.client.post("/api/chat_stream", json={
                "message": "question", "mode": "compare_system",
                "zero_model": "recursive/flint-v1.0:free",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"baseline", response.data)
            self.assertIn(b"local unavailable", response.data)
            stream.assert_called_once_with("question", "recursive/flint-v1.0:free", "test-key", generation_info=ANY)
            local.assert_called_once()
            cloud.assert_not_called()

    def test_local_stream_reports_generation_failure_without_hanging(self):
        tokenizer = Mock()
        tokenizer.eos_token_id = 1
        tokenizer.return_value = {}
        model = Mock()
        model.generate.side_effect = RuntimeError("out of memory")

        class FakeStreamer:
            def __init__(self, *args, **kwargs):
                self.ended = False

            def on_finalized_text(self, text, stream_end=False):
                self.ended = stream_end

            def __iter__(self):
                import time
                deadline = time.monotonic() + 3
                while not self.ended and time.monotonic() < deadline:
                    time.sleep(0.01)
                if not self.ended:
                    raise AssertionError("stream did not finish")
                return iter(())

        with patch.object(web_app, "local_ready", True), patch.object(web_app, "has_cuda", False), \
             patch.object(web_app, "has_adapter", True), patch.object(web_app, "model", model), \
             patch.object(web_app, "tokenizer", tokenizer), patch.object(web_app, "format_prompt", return_value="prompt"), \
             patch.object(web_app, "TextIteratorStreamer", FakeStreamer):
            result = list(web_app.generate_local_stream("Giải thích OAuth2 là gì?"))
            self.assertIn("Không thể sinh phản hồi local", result[-1])

    def test_zero_context_stream_reports_provider_limit_to_ui(self):
        import json
        def zero(message, model, key, generation_info):
            generation_info.update({"finish_reason": "length", "max_new_tokens": 4096})
            yield "partial"
        with patch.object(web_app, "stream_zero_context", side_effect=zero):
            response = self.client.post("/api/chat_stream", json={"message": "q", "mode": "zero_context"})
            events = [json.loads(line[6:]) for line in response.get_data(as_text=True).splitlines() if line.startswith("data: ")]
        done = next(event for event in events if event["type"] == "single_done")
        self.assertEqual(done["generation"]["finish_reason"], "length")

    def test_cloud_providers_do_not_retry_after_partial_response(self):
        import json
        import requests
        examples = [
            ("call_openrouter_stream", {"choices": [{"delta": {"content": "first"}}]}, {"openrouter_api_key": "test"}),
            ("call_claude_stream", {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "first"}}, {"anthropic_api_key": "test"}),
        ]
        for function, event, config in examples:
            with self.subTest(provider=function):
                def interrupted():
                    yield ("data: " + json.dumps(event)).encode()
                    raise requests.ConnectionError("lost")
                response = Mock(status_code=200)
                response.iter_lines.side_effect = interrupted
                info = {}
                with patch.multiple(web_app, **config), patch.object(web_app.requests, "post", return_value=response) as post:
                    chunks = list(getattr(web_app, function)("q", generation_info=info))
                self.assertEqual(chunks, ["first"])
                self.assertEqual(info["finish_reason"], "interrupted")
                self.assertEqual(post.call_count, 1)

    def test_gemini_never_combines_models_after_partial_stream_failure(self):
        import json
        import requests
        def interrupted():
            yield ("data: " + json.dumps({"candidates": [{"content": {"parts": [{"text": "first"}]}}]})).encode()
            raise requests.ConnectionError("stream interrupted")
        response = Mock(status_code=200)
        response.iter_lines.side_effect = interrupted
        info = {}
        with patch.object(web_app, "gemini_api_key", "test"), \
             patch.object(web_app, "_build_cloud_project_prompt", return_value="prompt"), \
             patch.object(web_app.requests, "post", return_value=response) as post:
            chunks = list(web_app.call_cloud_gemini_stream("q", generation_info=info))
        self.assertEqual(post.call_count, 1)
        self.assertEqual(chunks[0], "first")
        self.assertEqual(info["finish_reason"], "interrupted")

    def test_gemini_failure_does_not_forward_project_context_to_openrouter(self):
        response = Mock(status_code=503)
        with patch.object(web_app, "gemini_api_key", "test-gemini"), \
             patch.object(web_app, "openrouter_api_key", "test-openrouter"), \
             patch.object(web_app, "_build_cloud_project_prompt", return_value="project context"), \
             patch.object(web_app.requests, "post", return_value=response), \
             patch.object(web_app, "call_openrouter_stream") as openrouter, \
             patch.object(web_app, "call_cloud_gemini", return_value=("gemini unavailable", 0)):
            self.assertEqual(list(web_app.call_cloud_gemini_stream("question")), ["gemini unavailable"])
            openrouter.assert_not_called()


if __name__ == "__main__":
    unittest.main()
