import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

distill_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(distill_dir)
raw_input_file = os.path.join(distill_dir, "distilled_raw.json")
target_dataset_file = os.path.join(root_dir, "training", "dataset.jsonl")
if not os.path.exists(os.path.dirname(target_dataset_file)):
    target_dataset_file = os.path.join(root_dir, "dataset.jsonl")

print("=" * 70)
print("CÔNG CỤ NHẬP VÀ KIỂM ĐỊNH DỮ LIỆU CHƯNG CẤT TỪ AI LỚN")
print("=" * 70)

if not os.path.exists(raw_input_file):
    print(f"\n[HƯỚNG DẪN]: Hãy lưu kết quả do AI to (GPT-4 / Claude / Gemini) sinh ra vào file:")
    print(f"            -> '{raw_input_file}'")
    print("\nSau đó chạy lại script này: python 3_import_distilled_data.py\n")
    sys.exit(0)

print(f"Đang đọc dữ liệu từ: {raw_input_file}...")

try:
    with open(raw_input_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content.startswith("["):
            raw_data = json.loads(content)
        else:
            # Format từng dòng jsonl
            raw_data = [json.loads(line) for line in content.splitlines() if line.strip()]
except Exception as e:
    print(f"[LỖI]: Không thể parse JSON từ file '{raw_input_file}'. Chi tiết lỗi: {e}")
    sys.exit(1)

valid_samples = []
invalid_count = 0

for idx, item in enumerate(raw_data, 1):
    messages = item.get("messages")
    if not messages or len(messages) < 3:
        invalid_count += 1
        continue
    
    roles = [m.get("role") for m in messages]
    if roles != ["system", "user", "assistant"]:
        invalid_count += 1
        continue
        
    valid_samples.append(item)

print(f"-> Tổng số mẫu phát hiện : {len(raw_data)}")
print(f"-> Số mẫu hợp lệ chuẩn hóa: {len(valid_samples)}")
print(f"-> Số mẫu lỗi / bị bỏ qua : {invalid_count}")

if not valid_samples:
    print("[CẢNH BÁO]: Không tìm thấy mẫu hợp lệ nào để nhập!")
    sys.exit(1)

# Ghi vào dataset.jsonl (nối tiếp hoặc ghi đè an toàn)
backup_file = target_dataset_file + ".bak"
if os.path.exists(target_dataset_file):
    import shutil
    shutil.copyfile(target_dataset_file, backup_file)
    print(f"-> Đã sao lưu dataset cũ tại: {backup_file}")

with open(target_dataset_file, "w", encoding="utf-8") as f:
    for item in valid_samples:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\n[THÀNH CÔNG] Đã cập nhật {len(valid_samples)} mẫu chưng cất vào '{target_dataset_file}'!")
print("Bây giờ bạn có thể chạy 'python training/train_local.py --model 3b' để huấn luyện mô hình học tập dữ liệu mới này.")
print("=" * 70)
