import sys
import unittest
import tempfile
import json
from pathlib import Path
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation_core import build_messages, validate_reviews, summarize, paired_comparison
import evaluate


def result(case, variant, status="ok", repeat=0):
    return {"id": f"{case}/{variant}/{repeat}", "case_id": case, "variant": variant,
            "repeat": repeat, "status": status, "elapsed_seconds": 2.0}


class EvaluationCoreTests(unittest.TestCase):
    def test_identical_input_for_identical_context(self):
        self.assertEqual(build_messages("question", ""), [{"role": "user", "content": "question"}])
        contextual = build_messages("question", "source text")
        self.assertIn("source text", contextual[0]["content"])
        self.assertEqual(contextual, build_messages("question", "source text"))

    def test_connection_failures_and_unreviewed_results_are_not_scores(self):
        rows = [result("a", "base"), result("b", "base", "error"), result("c", "base")]
        reviews = [{"id": rows[0]["id"], "verdict": "pass", "reviewer": "reviewer", "evidence": "source checked"}]
        stats = summarize(rows, validate_reviews(rows, reviews))["base"]
        self.assertEqual((stats["attempts"], stats["errors"], stats["reviewed"]), (3, 1, 1))
        self.assertEqual(stats["pass_rate_percent"], 100.0)
        self.assertEqual(stats["pending"], 1)

    def test_review_must_reference_successful_unique_result_and_evidence(self):
        rows = [result("a", "base"), result("b", "base", "error")]
        for invalid in [
            [{"id": "missing", "verdict": "pass", "reviewer": "r", "evidence": "x"}],
            [{"id": rows[1]["id"], "verdict": "pass", "reviewer": "r", "evidence": "x"}],
            [{"id": rows[0]["id"], "verdict": "pass", "reviewer": "r", "evidence": ""}],
            [{"id": rows[0]["id"], "verdict": "pass", "reviewer": "r", "evidence": "x"}] * 2,
        ]:
            with self.assertRaises(ValueError):
                validate_reviews(rows, invalid)

    def test_paired_differences_use_only_reviewed_pairs(self):
        rows = [result("a", "base"), result("a", "lora"), result("b", "base"),
                result("b", "lora", "error"), result("c", "base"), result("c", "lora")]
        reviews = [{"id": rows[0]["id"], "verdict": "fail", "reviewer": "r", "evidence": "bad"},
                   {"id": rows[1]["id"], "verdict": "pass", "reviewer": "r", "evidence": "good"},
                   {"id": rows[2]["id"], "verdict": "pass", "reviewer": "r", "evidence": "ok"}]
        comparison = paired_comparison(rows, validate_reviews(rows, reviews), "base", "lora")
        self.assertEqual(comparison["paired_reviewed"], 1)
        self.assertEqual(comparison["difference_percentage_points"], 100.0)

    def test_code_pass_requires_explicit_compile_and_test_results(self):
        row = result("a", "base")
        row["kind"] = "code"
        review = {"id": row["id"], "verdict": "pass", "reviewer": "r", "evidence": "checked"}
        with self.assertRaises(ValueError):
            validate_reviews([row], [review])
        review.update(compile_status="pass", test_status="pass")
        self.assertEqual(validate_reviews([row], [review])[row["id"]]["verdict"], "pass")

    def test_suite_covers_project_general_and_ambiguous_cases(self):
        cases = evaluate.load_cases(evaluate.ROOT / "benchmark" / "cases.jsonl")
        self.assertGreaterEqual(len(cases), 48)
        self.assertTrue({"general_chat", "clarification", "code_generation"}.issubset({case["category"] for case in cases}))

    def test_select_cases_by_category_or_explicit_id(self):
        cases = evaluate.load_cases(evaluate.ROOT / "benchmark" / "cases.jsonl")
        general = evaluate.select_cases(cases, categories=["general_chat"], limit=2)
        self.assertEqual(len(general), 2)
        self.assertTrue(all(case["category"] == "general_chat" for case in general))
        picked = evaluate.select_cases(cases, case_ids=["AMB-01"])
        self.assertEqual([case["id"] for case in picked], ["AMB-01"])
        with self.assertRaises(ValueError):
            evaluate.select_cases(cases, case_ids=["missing"])
        with self.assertRaises(ValueError):
            evaluate.select_cases(cases, categories=["missing"])

    def test_runner_captures_four_ablation_variants_with_matching_prompts(self):
        class FakeLocal:
            model_id = "test-model"
            model_source = "test-source"
            device = "cpu"
            torch = SimpleNamespace(__version__="test", version=SimpleNamespace(cuda=None))
            def __init__(self, max_tokens):
                self.max_tokens = max_tokens
            def generate(self, messages, use_adapter):
                return {"answer": "generated", "elapsed_seconds": 1.0, "output_tokens": 2}

        with tempfile.TemporaryDirectory() as tmp, patch.object(evaluate, "LocalModel", FakeLocal):
            args = Namespace(cases=evaluate.ROOT / "benchmark" / "cases.jsonl", output_dir=Path(tmp),
                             modes="base,base_rag,lora,lora_rag", openrouter_model=None,
                             limit=1, repeats=1, max_tokens=4)
            self.assertEqual(evaluate.run(args), 0)
            folder = next(Path(tmp).iterdir())
            rows = [json.loads(line) for line in (folder / "results.jsonl").read_text(encoding="utf-8").splitlines()]
            by_mode = {row["variant"]: row for row in rows}
            self.assertEqual(len(rows), 4)
            self.assertEqual(by_mode["base"]["prompt_sha256"], by_mode["lora"]["prompt_sha256"])
            self.assertEqual(by_mode["base_rag"]["prompt_sha256"], by_mode["lora_rag"]["prompt_sha256"])
            context = json.loads((folder / "contexts.jsonl").read_text(encoding="utf-8"))
            self.assertEqual(context["context_sha256"], by_mode["base_rag"]["context_sha256"])
            summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
            self.assertIsNone(summary["base"]["pass_rate_percent"])
            reviews = [json.loads(line) for line in (folder / "reviews.jsonl").read_text(encoding="utf-8").splitlines()]
            for review in reviews:
                if review["id"] in (by_mode["base"]["id"], by_mode["lora"]["id"]):
                    review.update(verdict="pass" if review["id"] == by_mode["lora"]["id"] else "fail",
                                  reviewer="reviewer", evidence="checked against source")
            (folder / "reviews.jsonl").write_text("".join(json.dumps(review) + "\n" for review in reviews), encoding="utf-8")
            report = evaluate.make_report(folder)
            self.assertEqual(report["base"]["pass_rate_percent"], 0.0)
            self.assertEqual(report["lora"]["pass_rate_percent"], 100.0)
            self.assertIn("chưa hiển thị chênh lệch vì có dưới 5 cặp", (folder / "report.md").read_text(encoding="utf-8"))

    def test_runner_does_not_allow_random_or_paid_cloud_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = Namespace(cases=evaluate.ROOT / "benchmark" / "cases.jsonl", output_dir=Path(tmp),
                             modes="cloud_zero", openrouter_model="openrouter/free",
                             limit=1, repeats=1, max_tokens=4)
            with self.assertRaises(ValueError):
                evaluate.run(args)

    def test_cloud_rate_limit_and_unexpected_model_are_errors(self):
        with patch("requests.post", return_value=Mock(status_code=429)):
            outcome = evaluate.cloud_generate(build_messages("q"), "vendor/model:free", "key", 50)
            self.assertEqual((outcome["status"], outcome["error"]), ("error", "http_429"))
        response = Mock(status_code=200)
        response.json.return_value = {"model": "other/model:free", "choices": [{"message": {"content": "answer"}}]}
        with patch("requests.post", return_value=response):
            outcome = evaluate.cloud_generate(build_messages("q"), "vendor/model:free", "key", 50)
            self.assertEqual((outcome["status"], outcome["error"]), ("error", "unexpected_or_missing_model_id"))


if __name__ == "__main__":
    unittest.main()
