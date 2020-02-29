# -*- coding:utf-8 -*-

import time
import base64

from selenium.webdriver import Chrome, ActionChains, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from oppo.cv import find_distance
from oppo.paths import build_paths

bg_img = 'bg.png'
front_img = 'slide.png'

option = ChromeOptions()
option.add_argument('no-sandbox')
option.add_argument('disable-dev-shm-usage')
option.add_argument('--proxy-server=http://127.0.0.1:8080')

web = Chrome(ChromeDriverManager().install(), options=option)

try:
    web.get('http://e.oppomobile.com/market/login/index.html')

    # 移除webdriver
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => undefined,});'
    web.execute_script(script)

    time.sleep(1)

    # 保存canvas图片
    canvas = web.find_element_by_css_selector('#dx_captcha_basic_bg_1 > canvas')
    # get the canvas as a PNG base64 string
    canvas_base64 = web.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    # save to a file
    with open(bg_img, 'wb') as f:
        f.write(canvas_png)

    distance = find_distance(front_img, bg_img)
    print('distance: ', distance)

    paths = build_paths(distance)
    print('paths: ', len(paths), paths)

    time.sleep(1)

    # 找到滑块
    slide = web.find_element_by_css_selector('#dx_captcha_basic_slider-img-normal_1')

    # 按住滑块不放
    ActionChains(web).click_and_hold(slide).perform()
    time.sleep(0.5)

    for path in paths:
        x, y = path
        # 新建ActionChains对象防止累加位移
        ActionChains(web).move_by_offset(xoffset=x, yoffset=y).perform()

    # 释放滑块
    ActionChains(web).release().perform()


except Exception as e:
    print(e)
finally:
    time.sleep(1)
    web.close()
