
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
    # 获取窗口客户区的大小和位置
    client_rect = win32gui.GetClientRect(hwnd)

    # 获取窗口设备上下文
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建截图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, client_rect[2], client_rect[3])

    # 将截图对象选入截图DC
    saveDC.SelectObject(saveBitMap)

    # 截图
    # saveDC.BitBlt((0, 0), (client_rect[2], client_rect[3]), mfcDC, (0+8, 0+31), win32con.SRCCOPY)
    saveDC.BitBlt((0, 0), (client_rect[2], client_rect[3]), mfcDC, (0, 0), win32con.SRCCOPY)
    # 将截图转换为numpy数组
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype="uint8")
    img.shape = (client_rect[3], client_rect[2], 4)

    # bit图转mat图

    win32gui.DeleteObject(saveBitMap.GetHandle())
    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    # 释放内存
    return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)  # 转为RGB图返回


while True:
    alpha = 0.1
    # alpha = 0.03125
    # 获取窗口截图
    # img1 = window_capture(hwnd)

    hwnd_child = 0x0006026E

    # 获取窗口截图
    img1 = window_capture(hwnd_child)


    cv2.imshow("enc_img_end_decode", img1)
    if cv2.waitKey(1) == 27:  # 按ESC退出
        break

cv2.destroyAllWindows()
