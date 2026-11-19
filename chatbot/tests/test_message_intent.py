import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from message_intent import classify_message, project_retrieval_query


class MessageIntentTests(unittest.TestCase):
    def test_ambiguous_short_message_requests_clarification(self):
        for message in ("owo cf all", "abc xyz", "cái này"):
            with self.subTest(message=message):
                self.assertEqual(classify_message(message), "clarify")

    def test_general_chat_and_non_project_tasks_do_not_use_project_context(self):
        for message in ("xin chào", "xin chào bạn", "hello anh", "2+2 bằng mấy?", "viết một bài thơ về mùa thu",
                        "Giải thích OAuth2 là gì", "Viết Python tính Fibonacci",
                        "Hãy tạo dự án Flutter quản lý bán hàng", "Tạo dự án mới Flutter bán hàng"):
            with self.subTest(message=message):
                self.assertEqual(classify_message(message), "general")

    def test_explicit_project_requests_keep_context(self):
        for message in ("CourseDaoImpl kế thừa lớp nào?", "Sửa lỗi đăng nhập trong dự án này",
                        "Tạo module quản lý giảng viên", "Tài liệu dự án lưu ở đâu?",
                        "Viết phương thức findByPriceRange",
                        "Viết CourseRequestDTO và CourseResponseDTO chuẩn Jakarta Validation",
                        "Viết GenericSpecification và GenericSpecificationsBuilder tìm kiếm sinh viên"):
            with self.subTest(message=message):
                self.assertEqual(classify_message(message), "project")

    def test_explicit_followup_uses_only_relevant_previous_user_turn(self):
        project_history = [{"role": "user", "content": "CourseDaoImpl làm gì?"},
                           {"role": "assistant", "content": "Mô tả DAO."}]
        self.assertEqual(classify_message("giải thích thêm", project_history), "project")
        self.assertEqual(classify_message("giải thích thêm", project_history + [{"role": "user", "content": "nói rõ hơn"}]), "project")
        self.assertEqual(classify_message("giải thích thêm", [{"role": "user", "content": "OAuth2 là gì?"}]), "general")
        self.assertEqual(classify_message("viết thơ về biển", project_history), "general")
        self.assertEqual(classify_message("giải thích thêm"), "clarify")
        self.assertIn("CourseDaoImpl", project_retrieval_query("giải thích thêm", project_history))
        self.assertEqual(project_retrieval_query("viết thơ về biển", project_history), "viết thơ về biển")


if __name__ == "__main__":
    unittest.main()
