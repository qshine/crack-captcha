# -*- coding: utf-8 -*-

import cv2
import numpy as np


def show(name):
    cv2.imshow('test', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_distance(front_img: str, bg_img: str):
    front = cv2.imread(front_img)
    front_gray = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'gray_{front_img}', front_gray)

    # 滑块的长宽
    width, height = front.shape[:2]

    bg = cv2.imread(bg_img)
    gray_bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'gray_{bg_img}', gray_bg)
    gray_bg = abs(255 - gray_bg)
    cv2.imwrite(f'gray_sub_{bg_img}', gray_bg)

    # 匹配图像算法, 第三个参数是精度控制, 以下是精度最高的
    res = cv2.matchTemplate(gray_bg, front_gray, cv2.TM_CCOEFF_NORMED)
    # 注意opencv中的横轴是y, 纵轴是x
    x, y = np.unravel_index(np.argmax(res), res.shape)

    print(x, y)
    cv2.rectangle(bg, (y, x), (y + width, x + height), (0, 0, 255), 2)

    cv2.imwrite('bg_rectangle.png', bg)

    return y - 12


if __name__ == '__main__':
    find_distance('slide.png', 'bg.png')
