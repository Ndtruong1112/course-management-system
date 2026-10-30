# BỘ PROMPT CHƯNG CẤT TRI THỨC (TEACHER DISTILLATION PROMPT)

> **Hướng dẫn sử dụng:**
> 1. Mở một mô hình AI lớn (**GPT-4o**, **Claude 3.5 Sonnet**, **Gemini 1.5 Pro**, hoặc **DeepSeek**).
> 2. Đính kèm hoặc copy nội dung tệp `distillation/codebase_context.md` vào cuộc trò chuyện.
> 3. Copy toàn bộ nội dung prompt dưới đây và gửi cho AI:

---

```markdown
Bạn là một Kiến trúc sư Phần mềm Cao cấp (Senior Java Software Architect) kiêm Chuyên gia Huấn luyện Mô hình Ngôn ngữ Lớn (LLM Distillation Specialist).

Tôi đang đính kèm toàn bộ mã nguồn của dự án backend "Course Management System" được viết bằng Java 21, Spring Boot 3, Hibernate Generic DAO, JPA Specification và MinIO Storage.

### NHIỆM VỤ CỦA BẠN (KNOWLEDGE DISTILLATION):
Hãy đóng vai trò là "Mô hình Sư phụ" (Teacher Model) để chưng cất tri thức, tạo ra một bộ dữ liệu huấn luyện chất lượng cao (Instruction-Tuning Dataset) nhằm đào tạo một "Mô hình Học trò" (Student Model). 

Bộ dữ liệu này phải giúp mô hình học trò không chỉ hiểu sâu dự án hiện tại, mà còn **BIẾT TỰ TAY VIẾT CODE JAVA HOÀN CHỈNH KHI GẶP CÁC BÀI TOÁN TƯƠNG TỰ** (như Khách sạn, Bệnh viện, Thư viện, Bán hàng, Ngân hàng).

### QUY TẮC BẮT BUỘC KHI SINH CÂU TRẢ LỜI:
1. **LUÔN VIẾT MÃ NGUỒN JAVA THỰC TẾ**: Tuyệt đối không trả lời bằng văn mẫu lý thuyết suông hay chỉ gạch đầu dòng liệt kê tên class. Phải viết mã nguồn Java đầy đủ với `@Entity`, `@Table`, `@Id`, `@GeneratedValue`, Lombok `@Getter`, `@Setter`, `@Builder`...
2. **KẾ THỪA CHUẨN KIẾN TRÚC GENERIC DAO CỦA DỰ ÁN**:
   - Mọi lớp DAO mới phải kế thừa `HibernatePaginationSortingDao<Pk, Entity>`.
   - Sử dụng `EntityManager` để tạo các câu lệnh HQL/JPQL động an toàn kiểu dữ liệu.
3. **ĐA DẠNG HÓA CÁC CHỦ ĐỀ CHƯNG CẤT**:
   - **Nhóm 1 (Chuyển giao kiến trúc sang bài toán mới - 40%)**: Yêu cầu AI viết Entity, DAO, Service, Controller cho:
     * Quản lý Khách sạn (`Room`, `Reservation`).
     * Quản lý Thư viện (`Book`, `BorrowRecord`).
     * Quản lý Bán hàng (`Product`, `CustomerOrder`).
     * Quản lý Phòng khám/Bệnh viện (`Patient`, `Appointment`).
   - **Nhóm 2 (Truy vấn HQL & Dynamic Specification - 30%)**: Viết các hàm tìm kiếm lọc động đa điều kiện bằng JPA Criteria API và `GenericSpecification`.
   - **Nhóm 3 (Xử lý Lưu trữ MinIO & Versioning - 15%)**: Quản lý tài liệu, upload streaming, soft-delete, versioning.
   - **Nhóm 4 (Tối ưu hóa & Bắt lỗi Exception - 15%)**: `@RestControllerAdvice`, `@ExceptionHandler`, tạo custom exception.

### ĐỊNH DẠNG ĐẦU RA YÊU CẦU:
Hãy xuất kết quả dưới dạng mảng JSON (hoặc từng dòng JSONL) với cấu trúc:

[
  {
    "messages": [
      {
        "role": "system",
        "content": "Bạn là kỹ sư AI phần mềm cao cấp, chuyên gia kiến trúc Spring Boot 3, Java 21, Hibernate Generic DAO và JPA. Khi người dùng yêu cầu tạo dự án mới, viết chức năng hoặc giải quyết bài toán tương tự, bạn LUÔN LUÔN VIẾT MÃ NGUỒN JAVA ĐẦY ĐỦ, tuân thủ chính xác các quy chuẩn của dự án."
      },
      {
        "role": "user",
        "content": "<Câu hỏi hoặc yêu cầu lập trình thực tế>"
      },
      {
        "role": "assistant",
        "content": "<Mã nguồn Java chi tiết, giải thích kiến trúc sắc sảo, không dùng văn mẫu sáo rỗng>"
      }
    ]
  }
]
```
