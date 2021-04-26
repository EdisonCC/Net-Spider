# -*- coding:utf-8 -*-
import re
import json
import requests
from pyquery import PyQuery as pq

"""
目标APP：快手
目标url： APP图集分享链接/web端
爬取思路：
  - APP端：
    1. 通过APP里的分享获取视频url：https://v.kuaishou.com/cYRkmv
    2. url会经过两次重定向，然后跳转到真实地址
    3. 图片就是在其网页元素img标签中，不是经由异步请求获取的

  - WEB端：
    web端的快手图集经测试【必须要登录】才可以，若不登录的话，请求返回的结果是没有任何参考价值的
    url形如：
      - https://live.kuaishou.com/u/RR1718190/3x4bduuh4uqrbxa?did=web_088cf239f6654844bce30eb5e3c3abca
      - https://live.kuaishou.com/u/mx278516/3xahgx5ya7u366a?did=web_088cf239f6654844bce30eb5e3c3abca
            
"""


class KuaiPic(object):
    def __init__(self, url, cookies=""):
        self.url = url
        self.Cookies = cookies
        self.session = requests.session()

    def get_pic(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36 "
        }
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        try:
            if "/u/" in deal_url:
                api = deal_url
                headers["Cookie"] = self.Cookies
            else:
                # 获取第一次重定向
                response = self.session.get(url=deal_url, headers=headers, timeout=10)
                # 获取第二次重定向
                result = self.session.get(url=response.url, headers=headers, timeout=10)
                api = result.url
            # 从html上解析图片
            html5 = self.session.get(url=api, headers=headers, timeout=10)
            if html5.status_code == 200:
                doc = pq(html5.text)
                author = doc(".profile-user-name").text()
                description = doc(".profile-user-desc span").text()
                rows = doc(".long-mode img.long-mode-item")
                pics = []
                for row in rows.items():
                    pics.append(row.attr("src"))
                # 整理数据集
                info = {
                    "author": author,
                    "description": description,
                    "pictures": pics
                }
                return json.dumps(info, ensure_ascii=False)
            else:
                return json.dumps({"info": "发生未知错误，状态码：{}".format(html5.status_code)})
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    description = """
使用说明：
    存在两个参数(url，cookie)：
       - url表示带待传入链接，可以为APP分享或Web端
       - cookie可默认不传入，若为Web端链接，则必须传入，因为必须要登录才能获取正确的信息
    """
    print(description)
    ki_pic = KuaiPic(
        url="https://live.kuaishou.com/u/mx278516/3xahgx5ya7u366a?did=web_088cf239f6654844bce30eb5e3c3abca",
        cookies="your cookie")
    print(ki_pic.get_pic())