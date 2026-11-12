# Module Đánh Giá Thực Nghiệm Khoa Học (AI Benchmark Comparison)

Thư mục này chứa toàn bộ công cụ kiểm thử tự động, tập câu hỏi benchmark và báo cáo đánh giá thực nghiệm định lượng giữa 3 thực thể AI:

1. **AI Tiêu chuẩn ngoài thị trường (Zero Context)**: Đại diện cho các mô hình Cloud AI phổ biến khi chưa được cung cấp ngữ cảnh kiến trúc dự án.
2. **Base Model (Qwen2.5-Coder-3B gốc)**: Mô hình mã nguồn mở chưa qua fine-tuning.
3. **Hệ thống AI Dự án (Fine-tuned Model)**: Mô hình kết hợp LoRA Adapter và cơ chế điều phối ngữ cảnh kiến trúc doanh nghiệp.

---

## 📁 Cấu trúc thư mục

* `benchmark_comparison.py`: Script tự động thực thi 5 bài kiểm thử kiến trúc cốt lõi, chấm điểm 5 tiêu chí tự động và đo lường thời gian phản hồi.
* `chay_danh_gia_so_sanh.bat`: Script khởi chạy benchmark nhanh chỉ với 1 click, tự động mở bảng điều khiển trực quan sau khi hoàn tất.
* `BAO_CAO_SO_SANH_HIEU_QUA.md`: Báo cáo học thuật chi tiết phục vụ nghiệm thu đề tài/đồ án.
* `bao_cao_truc_quan.html`: Dashboard trực quan hiển thị biểu đồ Radar 5 chiều và Bar Chart phân tích tuân thủ kiến trúc.

---

## 🚀 Cách chạy benchmark

Từ thư mục này:
```bash
python benchmark_comparison.py
```
Hoặc nhấp đúp chạy file `chay_danh_gia_so_sanh.bat`.
Báo cáo HTML trực quan cũng có thể được xem trực tiếp từ giao diện Chatbot tại: `http://localhost:7860/benchmark-report`.
