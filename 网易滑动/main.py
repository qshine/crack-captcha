# -*- coding: utf-8 -*-

import cv2
import time
import requests
import numpy as np
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains

bg_img_name = 'bg_img.jpg'
front_img_name = 'front_img.jpg'

web = Chrome()
web.get('https://dun.163.com/trial/sense')

web.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/ul/li[2]').click()
time.sleep(2)

web.find_element_by_xpath(
    '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]').click()
time.sleep(3)

bg_img_src = web.find_element_by_xpath(
    '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[1]').get_attribute(
    'src')
front_img_src = web.find_element_by_xpath(
    '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/img[2]').get_attribute(
    'src')


def download_img(name, url):
    with open(name, 'wb') as f:
        f.write(requests.get(url).content)


download_img(bg_img_name, bg_img_src)
download_img(front_img_name, front_img_src)

bg = cv2.imread(bg_img_name)
bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'gray_{bg_img_name}', bg_gray)

# 对滑块处理只保留有效部分
front = cv2.imread(front_img_name)
front_gray = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'gray_{front_img_name}', front_gray)

front_gray = front_gray[front_gray.any(1)]
cv2.imwrite(f'new_gray_{front_img_name}', front_gray)

# 匹配图像算法, 第三个参数是精度控制, 以下是精度最高的
res = cv2.matchTemplate(bg_gray, front_gray, cv2.TM_CCOEFF_NORMED)

# 注意opencv中的横轴是y, 纵轴是x
x, y = np.unravel_index(np.argmax(res), res.shape)

print(x, y)

div = web.find_element_by_xpath(
    '/html/body/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[2]')

ActionChains(web).drag_and_drop_by_offset(div, xoffset=y // 1.6, yoffset=0).perform()

web.close()