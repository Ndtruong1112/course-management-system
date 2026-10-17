# 1. Base Model (Mô hình gốc - Chưa huấn luyện)

Thư mục này chứa script chạy trực tiếp mô hình nền **`Qwen/Qwen2.5-Coder-1.5B-Instruct`** nguyên bản, **CHƯA được gắn LoRA Adapter** của dự án.

### Mục đích:
- Dùng làm mốc đối chứng (Baseline) khi so sánh với mô hình đã fine-tune.
- Cho thấy mô hình gốc không biết gì về các cấu trúc riêng biệt của dự án như `SearchCriteria`, `HibernateGenericDao`, `DocumentServiceImpl`, v.v.

### Cách chạy:
```bash
python chat.py
```
