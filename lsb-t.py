import cv2

alpha = 0.1
# 加载两个图像
img1 = cv2.imread('R.jpg', 1)
img2 = cv2.imread('img.png', 1)
img1 = cv2.resize(img1, (800, 600))
img2 = cv2.resize(img2, (800, 600))
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)

# 将img1的像素值缩放到0-63区间
img1 = cv2.convertScaleAbs(img1, alpha=alpha)

# 将img2的像素值缩放到192-255区间
img2 = cv2.convertScaleAbs(img2, alpha=(1-alpha))

# 将img1和img2的像素值相加，得到加密图像
enc_img = cv2.add(img1, img2)

cv2.imshow("enc_img", enc_img)


# 加载两个图像
img1 = enc_img
img2 = cv2.imread('img.png', 1)
img1 = cv2.resize(img1, (1530, 835))
img2 = cv2.resize(img2, (1530, 835))
cv2.imshow("img1_decode", img1)
cv2.imshow("img2_decode", img2)
img2 = cv2.convertScaleAbs(img2, alpha=(1 - alpha))

enc_img = cv2.subtract(img1, img2)
# 将enc_img的像素值缩放到4倍
enc_img = cv2.convertScaleAbs(enc_img, alpha=(1/alpha))

cv2.imshow("lsb_——decode_0", enc_img)

# 保存加密图像
# cv2.imwrite('encrypted_img.png', enc_img)

# 等待按键
cv2.waitKey(0)

# 关闭窗口
cv2.destroyAllWindows()
