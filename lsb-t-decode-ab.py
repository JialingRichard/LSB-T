
import cv2
import numpy as np
import win32gui
import win32con
import win32api
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import win32ui

hwnd = win32gui.FindWindow("Main HighGUI class", "lsb_t_encode")


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

    #截取从左上角（0，0）长宽为（w，h）的图片
    title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)
    border_width = win32api.GetSystemMetrics(win32con.SM_CXSIZEFRAME)
    border_height = win32api.GetSystemMetrics(win32con.SM_CYSIZEFRAME)
    w = rctA[2] - rctA[0] - 2 * border_width
    h = rctA[3] - rctA[1] - title_bar_height - 2 * border_height

    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)
    # 高度saveDC，将截图保存到saveBitmap中
    # saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
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


while True:
    alpha = 0.25
    # 获取窗口截图
    img1 = window_capture(hwnd)

    # 加载两个图像
    img2 = cv2.imread('img.png', 1)
    img1 = cv2.resize(img1, (1530, 835))
    img2 = cv2.resize(img2, (1530, 835))
    cv2.imshow("img1_decode", img1)
    cv2.imshow("img2_decode", img2)
    img2 = cv2.convertScaleAbs(img2, alpha=(1 - alpha))

    enc_img = cv2.subtract(img1, img2)
    # 将enc_img的像素值缩放到4倍
    enc_img = cv2.convertScaleAbs(enc_img, alpha=(1/alpha))

    cv2.imshow("lsb_t_decode", enc_img)

    if cv2.waitKey(1) == 27:  # 按ESC退出
        break

cv2.destroyAllWindows()
