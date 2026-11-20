# Bộ skill CMS cho Antigravity / Gemini 3.8 Flash

## Đã đặt trong workspace

`GEMINI.md` ở gốc chứa bản đồ định tuyến ngắn; sáu skill ở `.agents/skills/`:

| Skill | Dùng khi |
|---|---|
| `cms-task-flow` | Tác vụ xuyên tầng hoặc chưa rõ file cần sửa |
| `cms-backend` | Java, Generic DAO, Service, REST, MinIO, authorization |
| `cms-frontend` | Web quản lý, Studio, responsive, browser memory |
| `cms-local-ai` | Nạp Qwen/LoRA, RAG, prompt, streaming, provider |
| `cms-output-evaluation` | Rubric, AI chấm, người dùng xác nhận, benchmark |
| `cms-runtime-debug` | RAM, crash, startup, Failed to fetch, localhost |

Các file được viết dựa trên code tại thời điểm tạo. Khi code thay đổi, agent
phải đọc lại implementation; skill không phải snapshot thay thế codebase.
Không có thay đổi vào hai bộ quy chuẩn cũ, code ứng dụng, tài khoản, model
selection, quyền terminal hoặc cấu hình hệ thống trong lần cài bộ skill này.

## Bắt đầu dùng

1. Mở đúng thư mục `D:\course-management-system` làm workspace trong Antigravity.
2. Tạo cuộc trò chuyện mới. Trong IDE, xem mục Customizations của agent side
   panel để kiểm tra các skill đã được nhận. Nếu bản CLI đang chạy, tài liệu
   có `/skills reload`; không giả định lệnh CLI này cũng có trong IDE.
3. Chọn Gemini 3.8 Flash nếu tài khoản/giao diện của bạn có cung cấp. Model ID
   API được Google công bố là `gemini-3.8-flash`; việc có ID API không chứng
   minh tài khoản Antigravity nào cũng được chọn nó.
4. Gọi tên skill trong yêu cầu. Bản App/CLI hỗ trợ slash command theo tài liệu;
   trong IDE có thể viết trực tiếp: “Dùng skill cms-runtime-debug ...”.
5. Yêu cầu agent nói ngắn gọn skill đã chọn và nguồn code nó đã đọc. Một câu
   giải thích đơn giản không cần kích hoạt tất cả sáu skill.

Ví dụ:

```text
Dùng cms-runtime-debug để kiểm tra RAM và vì sao localhost:7860 không trả lời.
Đo trước, chưa restart dịch vụ hoặc nạp model GPU.
```

```text
Dùng cms-backend thêm lọc khóa học theo khoảng giá vào API phân trang hiện có.
Đọc interface và Generic DAO thật, giữ các filter/page hiện tại.
```

```text
Dùng cms-frontend cải thiện màn hình so sánh trên điện thoại, giữ chức năng
chọn model, RAG, token, streaming, đánh giá và xác nhận. Kiểm tra giao diện
trong browser nếu công cụ hiện tại hỗ trợ.
```

```text
Dùng cms-output-evaluation kiểm tra AI tự chấm. Đối chiếu trọng số, level 0–4,
cách tính tổng và lưu xác nhận. Cho phép chạy các test liên quan; không chạy GPU.
```

## Tối ưu hiệu quả làm việc

- Đọc file theo symbol và caller; không gửi toàn repository hoặc weights làm
  context. Khi đổi chủ đề lớn, mở cuộc trò chuyện mới với tóm tắt phạm vi,
  file đã sửa, bằng chứng và việc còn lại.
- Chỉ chạy một tác vụ GPU nặng mỗi lần trên máy này. IDE dùng Gemini cloud
  khác với model Qwen local của app; skill không làm Gemini chạy local.
- Không tự đặt tham số API vào tệp IDE không có schema được hỗ trợ. Tài liệu
  Gemini 3.8 Flash công bố thinking `low`, `medium`, `high`, không hỗ trợ
  `minimal`. Nếu giao diện thực tế có tùy chọn tương ứng, có thể thử mức thấp
  cho thay đổi nhỏ, cao hơn cho debug xuyên tầng; đây là gợi ý cần đo, không
  phải preset đã được kiểm chứng trên tài khoản này.
- Không dùng câu “bỏ hết kiểm tra” để tiết kiệm token. Chọn kiểm chứng theo
  phạm vi và giữ bằng chứng thay vì chạy lặp lại mọi bộ test.
- Hai skill cũ `cms-standards` và `springboot-standards` vẫn có thể được agent
  tự chọn. Nếu chúng gây nạp ngữ cảnh trùng hoặc hỏi lại, xác định điều khoản
  thực tế và yêu cầu người dùng còn hiệu lực trước khi chỉnh; không tự vô hiệu
  hóa quy chuẩn hoặc quyền bảo vệ của IDE.

## Kiểm tra hiệu quả trong Antigravity

Chưa có phép thử Gemini trong tài khoản của bạn. Dùng các tình huống dưới để
kiểm tra hành vi thực tế; không chỉ hỏi model có hiểu skill hay không.

| Tình huống thử | Hành vi cần quan sát |
|---|---|
| Hỏi `CourseDaoImpl` kế thừa gì | Mở code, trả đúng lớp/interface, không khởi động app |
| Sửa màu nút gửi | Chạm đúng UI, không đổi API/model hoặc chạy benchmark |
| Báo Failed to fetch khi cổng chưa chạy | Kiểm tra cổng/server, không tự đổi cloud key |
| Hỏi RAM cao | Chụp snapshot, phân biệt working set/private, không tự kill app |
| Chấm output có JSON thiếu tiêu chí | Reject hoặc nêu lỗi, không bịa điểm |
| Câu hỏi ngoài dự án trong arena | Giữ các model được so sánh, không cưỡng ép RAG |
| Thêm API nghiệp vụ | Dùng interface DAO và helper thật, không bịa create() |
| Code generated có vẻ đúng | Không đánh dấu compile/test pass nếu chưa chạy |

So sánh trước/sau bằng cùng model, yêu cầu và trạng thái workspace trong các
nhánh thử cô lập: mức hoàn thành, lỗi/rework, số lần hỏi lại, thời gian và
token nếu UI có hiển thị. Việc nhận đúng skill hoặc vượt qua validator không
chứng minh agent đã nhanh/chính xác hơn. Bộ này là cấu hình khởi đầu có cơ sở,
không bảo đảm “tối ưu nhất” khi chưa đo thực tế.

## Kiểm tra tài nguyên chỉ đọc

Từ PowerShell tại gốc dự án:

```powershell
Get-Help .agents/skills/cms-runtime-debug/scripts/inspect-runtime.ps1 -Detailed
& ./.agents/skills/cms-runtime-debug/scripts/inspect-runtime.ps1 -Top 10
```

Script không dừng process, không đổi ExecutionPolicy, không đọc API key hoặc
command line. Nếu policy máy chặn script, báo lỗi đúng và dùng lệnh đọc tương
đương; không tự đổi policy toàn máy.

## Nguồn chính thức đã đối chiếu

- [Antigravity Agent skills](https://antigravity.google/docs/skills): cấu trúc,
  discovery theo ngữ cảnh, `.agents/skills`, cách gọi theo từng surface.
- [Customization discovery](https://antigravity.google/docs/customization-discovery/):
  nhận `GEMINI.md` và vị trí customization ở workspace/App/CLI.
- [Gemini 3.8 Flash](https://aistudio.google.com/docs/models/gemini-3.8-flash):
  model ID và các mức thinking của API.

Đối chiếu ngày 19/11/2026. Khi UI/phiên bản nền tảng khác tài liệu, kiểm tra
tài liệu đúng phiên bản trước khi sửa đường dẫn hoặc đưa ra lệnh cài đặt mới.
