# 2. Fine-tuned Model (Mô hình đã huấn luyện với Codebase)

Thư mục này chứa script chạy mô hình đã được nạp **LoRA Adapter** từ thư mục `outputs/course-management-lora-adapter`.

### Khả năng nổi bật:
- Nắm vững các Entity: `Course`, `Student`, `Document`.
- Biết cấu trúc lớp `SearchCriteria`, `GenericSpecification`, `GenericSpecificationsBuilder`.
- Sinh code Java chuẩn theo cấu trúc `IGenericDao` và `HibernatePaginationSortingDao`.
- Hiểu các quy tắc nghiệp vụ: Soft delete, Versioning, lưu trữ MinIO Object Storage.

### Cách chạy:
```bash
python chat.py
```
