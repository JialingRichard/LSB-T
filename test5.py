import cv2
import numpy as np

# 读取黑白视频
cap = cv2.VideoCapture('rick.mp4')

# 获取视频的宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义斑块的大小（宽度和高度）
block_size = 20
border_size = 1

# 计算斑块的数量
num_blocks_height = height // block_size
num_blocks_width = width // block_size

# 创建输出视频的编码器和写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('colorful_video.mp4', fourcc, 30.0, (width, height))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # 生成随机彩色小斑块
    colored_blocks = np.zeros((num_blocks_height, num_blocks_width, block_size, block_size, 3), dtype=np.uint8)
    for i in range(num_blocks_height):
        for j in range(num_blocks_width):
            color = np.random.randint(0, 256, 3, dtype=np.uint8)  # 随机生成RGB颜色
            colored_blocks[i, j, :, :, :] = color

    # 将斑块放置在原始帧上
    output_frame = np.copy(frame)
    for i in range(num_blocks_height):
        for j in range(num_blocks_width):
            start_row = i * block_size + border_size
            end_row = (i + 1) * block_size - border_size
            start_col = j * block_size + border_size
            end_col = (j + 1) * block_size - border_size
            output_frame[start_row:end_row, start_col:end_col, :] = colored_blocks[i, j, border_size:-border_size, border_size:-border_size, :]

    # 写入输出视频
    output_video.write(output_frame)

    cv2.imshow('Colorful Video', output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
output_video.release()
cv2.destroyAllWindows()
