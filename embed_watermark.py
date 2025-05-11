```python
import cv2
import numpy as np

# Hàm tạo ảnh đơn sắc 64x64
def create_colored_image(color, size=(64, 64)):
    img = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    img[:, :] = color  # Gán màu (BGR)
    return img

# Hàm nhúng thủy vân (ký tự "PTIT") vào khối 8x8
def embed_watermark(block, char):
    ascii_val = ord(char)
    # Nhúng 8 bit của ASCII vào 8 pixel đầu tiên (kênh B)
    for i in range(8):
        bit = (ascii_val >> i) & 1
        block[i // 4, i % 4, 0] = (block[i // 4, i % 4, 0] & ~1) | bit
    return block

# Tạo ảnh mẫu (màu đỏ)
sample_image = create_colored_image(color=(0, 0, 255))

# Kích thước khối và số lượng khối
block_size = 8
num_blocks = 64 // block_size  # 8 khối mỗi chiều

# Chuỗi thủy vân
watermark = "PTIT"

# Nhúng thủy vân vào ảnh
for i in range(num_blocks):
    for j in range(num_blocks):
        start_x, start_y = i * block_size, j * block_size
        end_x, end_y = start_x + block_size, start_y + block_size
        block = sample_image[start_x:end_x, start_y:end_y].copy()
        char = watermark[(i * num_blocks + j) % len(watermark)]
        sample_image[start_x:end_x, start_y:end_y] = embed_watermark(block, char)

# Lưu ảnh đã nhúng thủy vân
cv2.imwrite("watermarked_image.png", sample_image)

print("Đã nhúng thủy vân và lưu ảnh vào 'watermarked_image.png'.")
```