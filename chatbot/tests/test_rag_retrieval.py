import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rag_engine import CodebaseRAG


class RagRetrievalTests(unittest.TestCase):
    def test_document_storage_question_retrieves_both_storage_locations(self):
        root = Path(__file__).resolve().parents[2]
        rag = CodebaseRAG(str(root))
        context, _ = rag.format_context_block(
            "Dự án lưu nội dung file tài liệu và metadata tài liệu ở đâu? Trả lời ngắn.",
            top_k=3, max_chars=1800,
        )
        self.assertIn("MinIO", context)
        self.assertIn("MySQL", context)
        self.assertIn("metadata", context.lower())

    def test_application_configuration_does_not_index_secret_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "src/main/resources/application.properties"
            config.parent.mkdir(parents=True)
            config.write_text("spring.datasource.password=my-private-value\njwt.secret=signing-secret\nminio.endpoint=http://localhost:9000\n", encoding="utf-8")
            rag = CodebaseRAG(tmp)
            content = rag.docs[0]["content"]
            self.assertNotIn("my-private-value", content)
            self.assertNotIn("signing-secret", content)
            self.assertIn("minio.endpoint=http://localhost:9000", content)


if __name__ == "__main__":
    unittest.main()
