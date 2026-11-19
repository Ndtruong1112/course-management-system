import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openrouter_zero import DEFAULT_ZERO_MODEL, stream_zero_context


class ZeroContextTests(unittest.TestCase):
    def test_sends_only_current_question_to_exact_selected_model(self):
        response = Mock(status_code=200)
        response.iter_lines.return_value = [
            b'data: {"choices":[{"delta":{"content":"Hello"}}]}', b'data: [DONE]'
        ]
        post = Mock(return_value=response)
        self.assertEqual(list(stream_zero_context("question", DEFAULT_ZERO_MODEL, "test-key", post)), ["Hello"])
        self.assertEqual(post.call_count, 1)
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], DEFAULT_ZERO_MODEL)
        self.assertEqual(payload["messages"], [{"role": "user", "content": "question"}])
        response.close.assert_called_once()

    def test_finish_reason_and_interrupted_stream_are_recorded(self):
        response = Mock(status_code=200)
        response.iter_lines.return_value = [b'data: {"choices":[{"delta":{"content":"partial"},"finish_reason":null}]}',
                                            b'data: {"choices":[{"delta":{},"finish_reason":"length"}]}', b'data: [DONE]']
        info = {}
        self.assertEqual(list(stream_zero_context("q", DEFAULT_ZERO_MODEL, "key", Mock(return_value=response), generation_info=info)), ["partial"])
        self.assertEqual(info["finish_reason"], "length")
        response.iter_lines.return_value = [b'data: {"choices":[{"delta":{"content":"partial"}}]}']
        info = {}
        list(stream_zero_context("q", DEFAULT_ZERO_MODEL, "key", Mock(return_value=response), generation_info=info))
        self.assertEqual(info["finish_reason"], "interrupted")

    def test_rejects_unlisted_or_paid_model_without_network_call(self):
        post = Mock()
        result = list(stream_zero_context("q", "paid/model", "test-key", post))
        self.assertIn("không hợp lệ", result[0])
        post.assert_not_called()

    def test_rate_limit_does_not_silently_switch_model(self):
        response = Mock(status_code=429)
        post = Mock(return_value=response)
        result = list(stream_zero_context("q", DEFAULT_ZERO_MODEL, "test-key", post))
        self.assertIn("429", result[0])
        self.assertEqual(post.call_count, 1)
        response.close.assert_called_once()

    def test_sse_error_is_reported(self):
        response = Mock(status_code=200)
        response.iter_lines.return_value = [f'data: {json.dumps({"error": {"message": "failed"}})}'.encode()]
        result = list(stream_zero_context("q", DEFAULT_ZERO_MODEL, "test-key", Mock(return_value=response)))
        self.assertIn("báo lỗi", result[0])


if __name__ == "__main__":
    unittest.main()
