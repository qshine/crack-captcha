# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

front_name = 'front.png'
bg_name = 'bg.png'

front = cv.imread(front_name)
bg = cv.imread(bg_name)

tmp1 = front[4:28, 207:225]

# cv.imshow('front', tmp1)
# cv.waitKey(0)
#
# cv.destroyAllWindows()

# 灰度处理
front_gray = cv.cvtColor(tmp1, cv.COLOR_BGR2GRAY)
bg_gray = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)

cv.imwrite('gray_front_img.png', front_gray)
cv.imwrite('gray_bg_img.png', bg_gray)

res = cv.matchTemplate(bg_gray, front_gray, cv.TM_CCOEFF_NORMED)
max_loc = cv.minMaxLoc(res)
print(max_loc)

x, y = np.unravel_index(np.argmax(res), res.shape)

width, height = front_gray.shape
print(width, height)
print(x, y)

cv.rectangle(bg, (y, x), (y + 20, x + 25), (0, 0, 255), 2)

cv.imshow('test', bg)
cv.waitKey(0)

cv.destroyAllWindows()
