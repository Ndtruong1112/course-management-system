import gc
import sys
import torch

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def check_and_clean_vram():
    print("=" * 65)
    print("🧹 CÔNG CỤ KIỂM TRA & GIẢI PHÓNG BỘ NHỚ VRAM GPU")
    print("=" * 65)
    
    if not torch.cuda.is_available():
        print("[THÔNG BÁO]: Không tìm thấy GPU CUDA trên máy này. Đang chạy chế độ CPU.")
        print("=" * 65)
        return
        
    device_id = 0
    device_name = torch.cuda.get_device_name(device_id)
    total_mem = torch.cuda.get_device_properties(device_id).total_memory / (1024**3)
    
    # 1. Trạng thái VRAM trước khi dọn
    allocated_before = torch.cuda.memory_allocated(device_id) / (1024**3)
    reserved_before = torch.cuda.memory_reserved(device_id) / (1024**3)
    free_hardware, total_hardware = torch.cuda.mem_get_info(device_id)
    free_hardware_gb = free_hardware / (1024**3)
    
    print(f"🖥️  Phần cứng: {device_name}")
    print(f"• Tổng dung lượng VRAM:        {total_mem:.2f} GB")
    print(f"• VRAM đang sử dụng thực tế:   {allocated_before:.2f} GB")
    print(f"• VRAM bộ nhớ đệm (Reserved):  {reserved_before:.2f} GB")
    print(f"• VRAM hoàn toàn rảnh:         {free_hardware_gb:.2f} GB")
    print("-" * 65)
    
    # 2. Thực hiện dọn dẹp
    print("Đang tiến hành dọn dẹp rác (Garbage Collection) và xả CUDA Cache...")
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    torch.cuda.reset_peak_memory_stats()
    
    # 3. Trạng thái sau khi dọn
    allocated_after = torch.cuda.memory_allocated(device_id) / (1024**3)
    reserved_after = torch.cuda.memory_reserved(device_id) / (1024**3)
    free_hw_after, _ = torch.cuda.mem_get_info(device_id)
    free_hw_after_gb = free_hw_after / (1024**3)
    freed_gb = reserved_before - reserved_after
    
    if freed_gb > 0.05:
        print(f"✅ ĐÃ GIẢI PHÓNG THÀNH CÔNG: {freed_gb:.2f} GB VRAM!")
    else:
        print("✨ VRAM hiện tại đã ở trạng thái sạch và tối ưu.")
        
    print(f"🟢 VRAM khả dụng hiện tại:      {free_hw_after_gb:.2f} GB / {total_mem:.2f} GB")
    print("=" * 65)

if __name__ == "__main__":
    check_and_clean_vram()
