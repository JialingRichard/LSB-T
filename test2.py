import cv2
from selenium import webdriver
import numpy as np
import ctypes
from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome("./chromedriver.exe")    # Chrome浏览器

# chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
# driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
driver = webdriver.Chrome("./chromedriver.exe", options=options)
# 导航到目标网页
# driver.get('https://live.bilibili.com/13308358')

hwnd = ctypes.windll.user32.FindWindowW(None, driver.title)
print(f"Chrome窗口句柄：{hwnd}")

it = 0
while True:
    it+=1
    # current_handle = int(str(driver.current_window_handle), 16)
    # print(f"Current window handle: {current_handle}")
    # print("......>",it,".>1")
    # 按下Esc键退出循环
    if cv2.waitKey(1) == 27:
        break

# 释放资源
cv2.destroyAllWindows()
driver.quit()
