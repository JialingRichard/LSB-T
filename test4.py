import cv2
import numpy as np

# 读取原始图像
img = cv2.imread('S1.png')

def equal(px,px0):
    flag = True
    for i in range(0,3):
        # print(i)
        if(abs(int(px[i])-int(px0[i]))>10):
            flag = False


    return flag
def check(x,y,w,h,img):
    left=0
    right=0
    top=0
    bottom=0

    px = img[int(y+h/2),x]
    for i in range(0,w):
        px0 = img[int(y+h/2),x+i]
        if (equal(px,px0)):
            pass
        else:
            left = i
            break
    # print("left")
    # print(left)

    px = img[int(y + h / 2), x+w-1]
    for i in range(0, w):
        px0 = img[int(y + h / 2), x+w-1-i]
        if (equal(px, px0)):
            pass
        else:
            right = i
            break
    # print("right")
    # print(right)

    px = img[y, int(x + w / 2)]
    for i in range(0, h):
        px0 = img[y+i, int(x + w / 2)]
        if (equal(px, px0)):
            pass
        else:
            top = i
            break
    # print("top")
    # print(top)

    px = img[y+h-1, int(x + w / 2)]
    for i in range(0, h):
        px0 = img[y+h-1-i, int(x + w / 2)]
        if (equal(px, px0)):
            pass
        else:
            bottom = i
            break
    # print("bottom")
    # print(bottom)

    return left,right,top,bottom
def getOrigin(img):
    # 提取绿色边框的区域
    lower_green = np.array([0, 224, 0])
    upper_green = np.array([20, 255, 20])
    mask = cv2.inRange(img, lower_green, upper_green)
    # 找到绿色边框的轮廓
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 找到包含轮廓的最小矩形
    x, y, w, h = cv2.boundingRect(contours[0])


    left,right,top,bottom = check(x,y,w,h,img)

    # 截取原始图像中的区域
    cropped = img[y+top:y+h-bottom, x+left:x+w-right]
    # 在图像中绘制矩形框以显示截取的区域（可选）
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow('rectangle', img)
    # 显示结果图像
    # cv2.imshow('Result', cropped)
    # cv2.imwrite('S1_result.png', cropped)
    # cv2.waitKey(0)
    return cropped
getOrigin(img)