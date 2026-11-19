# Đánh giá trợ lý AI

Bộ đánh giá pilot gồm 48 tình huống trong `cases.jsonl`, có tiêu chí và tệp nguồn
để người đánh giá đối chiếu. Đây **chưa phải tập hold-out độc lập**: một số kiến
thức có thể đã xuất hiện trong dữ liệu huấn luyện. Không dùng kết quả để khẳng định
khả năng tổng quát hoặc chứng minh mã chạy được nếu chưa kiểm tra.

## Cấu hình so sánh

| Tên | Model | Adapter LoRA | Ngữ cảnh RAG |
|---|---|---|---|
| `base` | Qwen local gốc | Không | Không |
| `base_rag` | Qwen local gốc | Không | Có |
| `lora` | Qwen local | Có | Không |
| `lora_rag` | Qwen local | Có | Có |
| `cloud_zero` | OpenRouter được chỉ định | Không | Không |
| `cloud_rag` | OpenRouter được chỉ định | Không | Cùng nội dung RAG với local |

Cùng một câu hỏi và nội dung RAG được dùng trong các cặp tương ứng. Local dùng
greedy decoding; Cloud đặt temperature 0 nhưng provider có thể không tái lập hoàn
toàn. Các model có tokenizer khác nhau nên cùng giới hạn token không tương đương
độ dài văn bản. LoRA và base dùng chung trọng số gốc, chỉ bật/tắt adapter.

## Chạy thử

Benchmark nạp một bản model riêng, không dùng chung model đã nạp trong chatbot;
nếu cả hai cùng chạy, RAM và VRAM có thể tăng đáng kể. Nên đóng chatbot hoặc
khởi động lại chatbot ở trạng thái chưa nạp model trước khi chạy benchmark.
Khi không có CUDA, benchmark không tự nạp model lên CPU. Chỉ đặt biến môi trường
`LOCAL_ALLOW_CPU=true` nếu bạn chủ động muốn chạy CPU và có đủ RAM.

Từ thư mục gốc dự án, chạy một câu với bốn cấu hình local:

```powershell
python -X utf8 benchmark/evaluate.py run --limit 1 --max-tokens 128
```

Chạy toàn bộ 48 câu local (có thể mất nhiều thời gian):

```powershell
python -X utf8 benchmark/evaluate.py run --max-tokens 512
```

Chạy riêng câu hỏi ngoài dự án và câu thiếu thông tin với bốn cấu hình local:

```powershell
python -X utf8 benchmark/evaluate.py run --category general_chat --category clarification --max-tokens 256
```

Chọn câu cụ thể bằng `--case-id AMB-01` (có thể lặp lại tham số). RAG trong
benchmark được áp dụng theo từng cấu hình, kể cả câu hỏi chung; nếu không truy
xuất được tệp, báo cáo hiển thị 0 tệp. Điều này đo cấu hình RAG cưỡng bức, không
phải chính sách RAG tự động trong giao diện chat.

Để bổ sung Cloud, đặt `OPENROUTER_API_KEY` trong môi trường hoặc `.env` rồi chọn
một ID `:free` cụ thể. Không dùng Free Router ngẫu nhiên cho benchmark:

```powershell
python -X utf8 benchmark/evaluate.py run --limit 1 --max-tokens 512 --modes base,base_rag,lora,lora_rag,cloud_zero,cloud_rag --openrouter-model particle-ai/particle-1:free
```

**Cloud RAG gửi các đoạn mã/tài liệu được truy xuất tới OpenRouter và provider.**
Chỉ bật `cloud_rag` khi được phép chia sẻ dữ liệu. Có thể chạy `cloud_zero` riêng.
Lỗi quota, mạng, response rỗng và lỗi tải model được lưu riêng, không được tính
là câu trả lời sai. Các file run chứa câu hỏi/câu trả lời và có thể chứa thông
tin dự án; thư mục `runs/` được Git bỏ qua.

## Đánh giá câu trả lời

Mỗi lượt tạo thư mục `benchmark/runs/<run-id>/`:

- `manifest.json`: cấu hình, hash bộ câu hỏi và corpus, Git, model, adapter, môi trường.
- `cases.json`: câu hỏi, tiêu chí kiểm tra và nguồn đối chiếu.
- `contexts.jsonl`: snapshot ngữ cảnh RAG thực tế cho từng câu, dùng để tái lập.
- `results.jsonl`: câu trả lời, trạng thái, thời gian, số token và hash prompt/RAG.
- `reviews.jsonl`: mẫu đánh giá; ban đầu tất cả là `pending`.
- `report.md` và `summary.json`: thống kê tình trạng và kết quả đã được chấm.

Mở `/benchmark-report`, chọn lần chạy rồi mở câu hỏi để xem tiêu chí, nguồn và
các câu trả lời. Mục **Đánh giá phản hồi này** cho phép ghi người chấm, bằng
chứng và trạng thái compile/test; báo cáo trên web tự tính lại sau khi lưu.
Nếu một trang khác đã sửa đánh giá, hãy tải lại trước khi lưu để tránh ghi đè.
`summary.json` và `report.md` là bản xuất tĩnh, cần chạy lệnh `report` bên dưới
để cập nhật chúng. Chấm trực tiếp trong chat vẫn lưu riêng trên trình duyệt;
không tự xem là kết quả benchmark.

Ngoài ra, có thể sửa đúng dòng tương ứng trong `reviews.jsonl` sau khi đối chiếu
`checks` và `sources`:

```json
{"id":"ARCH-01/base/0","verdict":"pass","reviewer":"ten-nguoi-cham","evidence":"Đối chiếu CourseDaoImpl.java: lớp cha và interface đều đúng","compile_status":"not_applicable","test_status":"not_applicable"}
```

`verdict` là `pass`, `fail` hoặc `pending`; `pass`/`fail` yêu cầu tên người chấm
và bằng chứng. Với bài `kind=code`, muốn đánh dấu `pass` phải ghi cả
`compile_status` và `test_status` là `pass` sau khi thực sự kiểm tra trong môi
trường cô lập. Giá trị hợp lệ: `pass`, `fail`, `not_run`, `not_applicable`. Các
trường là **khai báo của người đánh giá**, không phải bằng chứng tự động; lưu
đường dẫn log hoặc chi tiết trong `evidence`. Không tự chạy mã do model tạo.

Sau khi chấm, cập nhật báo cáo:

```powershell
python -X utf8 benchmark/evaluate.py report benchmark/runs/<run-id>
```

Tỷ lệ đạt chỉ tính trên câu thành công đã được chấm. Chênh lệch giữa hai cấu hình
chỉ tính trên cặp **cùng câu và cùng lần lặp**, có kết quả chấm ở cả hai phía.
Lượt lỗi được thống kê riêng. `--repeats` hỗ trợ lặp, nhưng local greedy và Cloud
có thể khác tính ngẫu nhiên; nên giải thích điều kiện khi so sánh. Thời gian local
không gồm tải model; Cloud có độ trễ mạng. Không kết luận ý nghĩa thống kê từ một
vài mẫu. Báo cáo chỉ hiện số lượng khi có dưới 5 mẫu/cặp; đây là ngưỡng hiển thị,
không phải bảo đảm rằng từ 5 mẫu trở lên là đủ cho kết luận thống kê.

`benchmark_comparison.py` và `scripts/run_benchmark.bat` giữ đường chạy tương
thích, mặc định chỉ chạy thử một câu; `training/evaluate_model.py` cũ bị vô hiệu
hóa vì tính "độ chính xác" bằng cách khớp từ khóa. Các báo cáo cũ được giữ để
tham khảo lịch sử và gắn cảnh báo, không dùng làm kết luận khoa học.
