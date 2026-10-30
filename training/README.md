# Module Huấn Luyện & Tinh Chỉnh Mô Hình (AI Training & Evaluation)

Thư mục này quản lý toàn bộ quy trình sinh dữ liệu (Dataset Generation), huấn luyện tinh chỉnh mô hình cục bộ bằng QLoRA 4-bit (Fine-tuning), kiểm thử tự động, và quản lý tài nguyên bộ nhớ GPU.

---

## 📁 Danh sách tệp & Chức năng

| Tệp tin | Chức năng chi tiết |
| :--- | :--- |
| `generate_dataset.py` | Quét tự động codebase Java (Entities, DAOs, Services, DTOs, Rest Controllers) và sinh tập câu hỏi/trả lời chuẩn hóa theo phong cách ChatML. |
| `dataset.jsonl` | Tập dữ liệu huấn luyện đã sinh, chứa các mẫu Q&A tuân thủ 100% quy chuẩn kiến trúc của dự án. |
| `train_local.py` | Script huấn luyện QLoRA 4-bit (NF4) trên GPU NVIDIA (RTX 4050 6GB), xuất LoRA adapter vào thư mục `outputs/course-management-lora-adapter`. |
| `test_model.py` | Kiểm thử tương tác hoặc chạy bộ câu hỏi ngẫu nhiên với mô hình sau khi fine-tuning. |
| `evaluate_model.py` | Bộ đo lường định lượng tỷ lệ tuân thủ quy chuẩn (Generic DAO, HQL, Package, DTO...), xuất kết quả ra `eval_report.json`. |
| `eval_report.json` | Báo cáo chi tiết kết quả đánh giá tự động. |
| `clean_vram.py` | Công cụ giải phóng bộ nhớ đệm VRAM và dọn dẹp CUDA Cache của GPU. |
| `Course_Management_AI_Colab.ipynb` | Jupyter Notebook hỗ trợ huấn luyện trên đám mây miễn phí (Google Colab T4 GPU). |

---

## 🚀 Hướng dẫn nhanh

### 1. Sinh lại dữ liệu huấn luyện từ Codebase mới
```bash
python generate_dataset.py
```

### 2. Huấn luyện mô hình LoRA trên GPU cục bộ
```bash
python train_local.py --model 3b --steps 100
```

### 3. Kiểm thử chất lượng câu trả lời
```bash
python test_model.py --num 3
```

### 4. Đánh giá độ chính xác tổng thể
```bash
python evaluate_model.py
```

### 5. Dọn dẹp VRAM nếu cần
```bash
python clean_vram.py
```
