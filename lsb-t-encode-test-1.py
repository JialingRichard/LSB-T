
import cv2
import numpy as np
import win32gui
import win32con
import win32api
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import win32ui
import subprocess
hwnd = win32gui.FindWindow("SDL_app", "Hearts of Iron IV (DirectX 11)")

# hwnd = win32gui.FindWindow("SDL_app", "Stellaris")
def change(ll):
    for index in range(len(ll)):
        i = ll[index][0]
        j = ll[index][1]

        if (i % 2 == 0):
            i += 1
        else:
            i -= 1

        if (j % 2 == 0):
            j += 1
        else:
            j -= 1

        ll[index] = (i, j)
    return ll
def random_change(image, size=8):

    # 获取图像的宽度和高度
    height, width, _ = image.shape

    # 定义每个小块的宽度和高度
    block_width = width // size
    block_height = height // size

    # 切割图像并存储到列表中
    blocks = []
    index_list = []  # 索引列表

    for i in range(size):
        for j in range(size):
            block = image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width]
            blocks.append(block)
            index_list.append((i, j))  # 记录小块的索引


    # 打乱小块的顺序
    # shuffled_index_list = np.random.permutation(index_list)



    shuffled_index_list = change(index_list)

    # 按照打乱后的索引列表重新组合小块
    restored_image = np.zeros_like(image)
    # cv2.imshow('Restored Image1', restored_image)
    for k, (i, j) in enumerate(shuffled_index_list):
        block = blocks[k]
        restored_image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width] = block

    # 显示图像
    # cv2.imshow('Restored Image', restored_image)
    return restored_image
def window_capture(hwnd):
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()
    # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()
    # 创建bigmap准备保存图片
    rctA = win32gui.GetWindowRect(hwnd)
    w = rctA[2] - rctA[0]
    h = rctA[3] - rctA[1]
    # 获取图片大小
    # 截取从左上角（0，0）长宽为（w，h）的图片

    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype="uint8")
    img.shape = (h, w, 4)
    # bit图转mat图

    win32gui.DeleteObject(saveBitMap.GetHandle())
    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    # 释放内存
    return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)  # 转为RGB图返回


path = "D:/sys_video/rick-2-done.mp4"
path = "rick-2.mp4"
# path = "D:/sys_video/rick-test2.mp4"
cap = cv2.VideoCapture(path)
frame_counter = 0
video_file = path
# # FFmpeg 命令
# ffmpeg_cmd = f"ffplay  -nodisp -vn  {path}"
# subprocess.Popen(ffmpeg_cmd)

while True:
    alpha = 0.3
    # alpha = 0.03125

    ret, img2 = cap.read()
    # frame = cv2.resize(frame, (725, 500))
    frame_counter += 1
    if frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        frame_counter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # subprocess.Popen(ffmpeg_cmd)
    # cv2.imshow("frame", img2)

    # 获取窗口截图
    img1 = window_capture(hwnd)
    # img1 = cv2.imread('hoi.jpg', 1)
    img1 = random_change(image=img1, size=16)

    img3 = cv2.imread('img.png', 1)
    width = int(1530/2)
    height = int(835)
    img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))
    img3 = cv2.resize(img3, (width, height))


    # img1_bk = cv2.resize(img1, (550, 300))
    # img2_bk = cv2.resize(img2, (550, 300))
    # cv2.imshow("img1", img1)
    # cv2.imshow("img1_bk", img1_bk)
    # cv2.imshow("img2", img2)
    # 将img1的像素值缩放到0-63区间
    # img3_temp = cv2.convertScaleAbs(img3, alpha=beta)
    # cv2.imshow("img3_temp", img3_temp)
    # # 将img2的像素值缩放到192-255区间
    # img2_temp = cv2.convertScaleAbs(img2, alpha=(1 - beta))
    # img2 = cv2.add(img3_temp, img2_temp)
    # cv2.imshow("lsb_t_encode2", img2)


    # 将img1的像素值缩放到0-63区间
    img1_temp = cv2.convertScaleAbs(img1, alpha=alpha)
    # 将img2的像素值缩放到192-255区间
    img2_temp = cv2.convertScaleAbs(img2, alpha=(1-alpha))
    # 将img1和img2的像素值相加，得到加密图像
    enc_img = cv2.add(img1_temp, img2_temp)
    #水平翻转
    enc_img = cv2.flip(enc_img, 1)
    #水平拼接
    enc_img = cv2.hconcat([img2, enc_img])

    # enc_img_bk = cv2.resize(enc_img, (960, 540))
    # enc_img = cv2.copyMakeBorder(enc_img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[0, 255, 0])
    cv2.imshow("lsb_t_encode", enc_img)
    # cv2.imshow("lsb_t_encode_bk", enc_img_bk)
    if cv2.waitKey(1) == 27:  # 按ESC退出
        break

cv2.destroyAllWindows()
