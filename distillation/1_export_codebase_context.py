import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src", "main", "java")
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codebase_context.md")

print("=" * 70)
print("BẮT ĐẦU GOM MÃ NGUỒN DỰ ÁN ĐỂ CHUẨN BỊ CHƯNG CẤT TRI THỨC")
print("=" * 70)

collected_files = []

for root, _, files in os.walk(src_dir):
    for f in sorted(files):
        if f.endswith(".java"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                    collected_files.append((rel_path, content))
            except Exception as e:
                print(f"Lỗi đọc file {rel_path}: {e}")

# Đọc thêm application.properties
app_prop = os.path.join(base_dir, "src", "main", "resources", "application.properties")
if os.path.exists(app_prop):
    rel_p = os.path.relpath(app_prop, base_dir).replace("\\", "/")
    with open(app_prop, "r", encoding="utf-8") as fp:
        collected_files.append((rel_p, fp.read()))

print(f"-> Đã thu thập {len(collected_files)} tệp mã nguồn cốt lõi.")

with open(output_file, "w", encoding="utf-8") as out:
    out.write("# TOÀN BỘ MÃ NGUỒN DỰ ÁN COURSE MANAGEMENT SYSTEM\n\n")
    out.write("Tài liệu này tổng hợp toàn bộ các file Java, Generic DAO, MinIO Storage, JPA Specification và cấu hình để nạp vào Mô hình AI Lớn (Teacher Model) phục vụ Chưng cất Tri thức (Knowledge Distillation).\n\n")
    out.write("---\n\n")
    
    for path, code in collected_files:
        out.write(f"## File: `{path}`\n\n")
        lang = "properties" if path.endswith(".properties") else "java"
        out.write(f"```{lang}\n{code.strip()}\n```\n\n---\n\n")

print(f"XUẤT THÀNH CÔNG: {output_file}")
print("File này đã sẵn sàng để bạn đính kèm hoặc copy vào ChatGPT / Claude / Gemini!")
print("=" * 70)
