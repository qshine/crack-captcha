# -*- coding: utf-8 -*-

import cv2
import numpy as np

def find_distance(front_img, bg_img):
    front = cv2.imread(front_img)
    front_gray = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'gray_{front_img}', front_gray)

    bg = cv2.imread(bg_img)
    gray_bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'gray_{bg_img}', gray_bg)

    # 找出滑块最小的图片
    front_gray = front_gray[front_gray.any(1)]
    cv2.imwrite(f'gray_min_{front_img}', front_gray)


    # 匹配图像算法, 第三个参数是精度控制, 以下是精度最高的
    res = cv2.matchTemplate(gray_bg, front_gray, cv2.TM_CCOEFF_NORMED)
    # 注意opencv中的横轴是y, 纵轴是x
    x, y = np.unravel_index(np.argmax(res), res.shape)

    print(x, y)
    cv2.rectangle(bg, (y, x), (y + front_gray.shape[1], x + front_gray.shape[0]), (0, 0, 255), 2)
    cv2.imshow('test', bg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

find_distance('front_img.jpg', 'bg_img.jpg')