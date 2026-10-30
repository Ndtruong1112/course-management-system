# Phân hệ Chưng cất Tri thức (Knowledge Distillation Module)

Thư mục này được thiết kế độc lập nhằm triển khai kỹ thuật **Chưng cất tri thức (Knowledge Distillation)** từ Mô hình Ngôn ngữ Lớn đầu ngành (Teacher LLM: GPT-4o / Claude 3.5 Sonnet / Gemini 1.5 Pro) sang Mô hình Cục bộ (Student Model: Qwen2.5-Coder-3B).

---

## 🎯 1. Ý nghĩa và Cơ sở Khoa học (Dùng để báo cáo với Thầy)

* **Vấn đề thực tế**: Codebase nội bộ của doanh nghiệp/trường học thường chỉ có khoảng 40–50 file Java. Nếu chỉ huấn luyện đơn thuần trên các file này, mô hình nhỏ rất dễ bị **học vẹt (overfitting)** và không thể tự suy luận để viết code cho các bài toán tương tự.
* **Giải pháp Chưng cất Tri thức**:
  1. Sử dụng **Teacher Model** (mô hình ngôn ngữ có hàng trăm tỷ tham số) nạp toàn bộ 44 file Java của dự án.
  2. Yêu cầu Teacher Model đóng vai Kiến trúc sư phần mềm, phân tích và sinh ra hàng trăm bài tập lập trình Java mẫu mực (chuyển giao kiến trúc sang bài toán Khách sạn, Thư viện, Bán hàng, Ngân hàng).
  3. Lấy dữ liệu tinh hoa đó huấn luyện cho **Student Model (Qwen2.5-Coder-3B)** chạy cục bộ trên card đồ họa RTX 4050.
* **Kết quả đạt được**: Mô hình học trò 3B chạy siêu nhanh trên máy tính cá nhân nhưng lại sở hữu **năng lực tư duy lập trình và khả năng sinh mã nguồn Java của mô hình lớn**.

---

## 🛠️ 2. Quy trình thực hiện từng bước

### Bước 1: Gom mã nguồn dự án thành file ngữ cảnh
Chạy lệnh:
```bash
python 1_export_codebase_context.py
```
-> Kết quả sinh ra file `codebase_context.md` chứa toàn bộ 45 file Java và file cấu hình của dự án.

### Bước 2: Chưng cất dữ liệu bằng AI lớn (Teacher)
1. Mở ChatGPT (GPT-4o), Claude 3.5 Sonnet hoặc Gemini.
2. Mở file `2_teacher_prompt.md`, copy toàn bộ nội dung prompt và đính kèm file `codebase_context.md`.
3. Nhận kết quả JSON do AI lớn sinh ra và lưu vào file:
   `distillation/distilled_raw.json`

### Bước 3: Kiểm định và nạp dữ liệu
Chạy lệnh:
```bash
python 3_import_distilled_data.py
```
-> Script sẽ tự động kiểm tra định dạng các mẫu, chuẩn hóa và nạp vào `training/dataset.jsonl`.

### Bước 4: Huấn luyện mô hình học trò
Từ thư mục gốc dự án chạy:
```bash
python training/train_local.py --model 3b
```
-> Mô hình 3B sẽ được trang bị toàn bộ tri thức chưng cất từ mô hình lớn!
