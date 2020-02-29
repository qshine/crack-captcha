# -*- coding:utf-8 -*-

'''
mitmdump -s script.py
'''


def response(flow):
    log = ctx.log
    log.info(flow.request.url)
    url = flow.request.url
    if '/captcha/api/p2' in url:
        response = flow.response
        # 获取响应内容
        content = response.content
        with open('slide.png', 'wb') as f:
            f.write(content)
    elif '/captcha/api/p1' in url:
        response = flow.response
        # 获取响应内容
        content = response.content
        with open('bg.png', 'wb') as f:
            f.write(content)

