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
    for i in range(8):
        bit = (ascii_val >> i) & 1
        block[i // 4, i % 4, 0] = (block[i // 4, i % 4, 0] & ~1) | bit
    return block

# Tạo ba ảnh mẫu (đỏ, xanh, vàng)
img1 = create_colored_image(color=(0, 0, 255))  # Đỏ
img2 = create_colored_image(color=(0, 255, 0))  # Xanh
img3 = create_colored_image(color=(255, 0, 0))  # Vàng

# Kích thước khối và số lượng khối
block_size = 8
num_blocks = 64 // block_size

# Nhúng thủy vân vào từng ảnh
watermark = "PTIT"
for img in [img1, img2, img3]:
    for i in range(num_blocks):
        for j in range(num_blocks):
            start_x, start_y = i * block_size, j * block_size
            end_x, end_y = start_x + block_size, start_y + block_size
            block = img[start_x:end_x, start_y:end_y].copy()
            char = watermark[(i * num_blocks + j) % len(watermark)]
            img[start_x:end_x, start_y:end_y] = embed_watermark(block, char)

# Lưu các ảnh đã nhúng thủy vân
cv2.imwrite("img1_watermarked.png", img1)
cv2.imwrite("img2_watermarked.png", img2)
cv2.imwrite("img3_watermarked.png", img3)

# Tạo ảnh cắt dán
collage_img = np.zeros((64, 64, 3), dtype=np.uint8)
for i in range(num_blocks):
    for j in range(num_blocks):
        start_x, start_y = i * block_size, j * block_size
        end_x, end_y = start_x + block_size, start_y + block_size
        if i < num_blocks // 2 and j < num_blocks // 2:
            collage_img[start_x:end_x, start_y:end_y] = img1[start_x:end_x, start_y:end_y]
        elif i >= num_blocks // 2 and j < num_blocks // 2:
            collage_img[start_x:end_x, start_y:end_y] = img2[start_x:end_x, start_y:end_y]
        else:
            collage_img[start_x:end_x, start_y:end_y] = img3[start_x:end_x, start_y:end_y]

# Lưu ảnh cắt dán
cv2.imwrite("collage_image.png", collage_img)

print("Đã tạo ảnh cắt dán và lưu vào 'collage_image.png'.")
```