```python
import cv2
import numpy as np
import sys

# Hàm trích xuất thủy vân từ khối 8x8
def extract_watermark(block):
    ascii_val = 0
    for i in range(8):
        bit = block[i // 4, i % 4, 0] & 1
        ascii_val |= bit << i
    try:
        return chr(ascii_val)
    except ValueError:
        return '?'

# Kiểm tra tham số dòng lệnh
if len(sys.argv) != 2:
    print("Cách dùng: python3 extract_watermark.py <đường_dẫn_ảnh>")
    sys.exit(1)

image_path = sys.argv[1]

# Đọc ảnh
image = cv2.imread(image_path)
if image is None:
    print(f"Không thể đọc ảnh: {image_path}")
    sys.exit(1)

# Kích thước khối và số lượng khối
block_size = 8
num_blocks = 64 // block_size

# Trích xuất thủy vân
extracted_watermarks = []
for i in range(num_blocks):
    row = []
    for j in range(num_blocks):
        start_x, start_y = i * block_size, j * block_size
        end_x, end_y = start_x + block_size, start_y + block_size
        block = image[start_x:end_x, start_y:end_y]
        watermark_char = extract_watermark(block)
        row.append(watermark_char)
    extracted_watermarks.append(row)

# In lưới thủy vân
print("Thủy vân trích xuất từ ảnh (8x8 khối):")
for row in extracted_watermarks:
    print(" ".join(row))
```