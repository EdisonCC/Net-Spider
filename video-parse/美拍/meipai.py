# -*- coding:utf-8 -*-
import re
import json
import base64
import execjs
import requests

"""
目标APP：美拍视频
目标url：APP短视频分享链接或PC网址
爬取思路：
    1. 视频的url是在网页源代码中，但是加密的
    2. 视频url解密后，还要继续跳转2次（每次请求的headers请求头是不同的），才会获取最终视频url地址
    3. 暂时还没有在PC端找到完全无水印的接口地址，PC端解析后的有无水印情况依据于源视频是否有水印
"""

"""
# 方法一：
class MeiPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        with open("static/loveword/js/meipai_encrypt.js", "r", encoding="utf-8") as f:
            resource = f.read()
        self.ctx = execjs.compile(resource)
    def get_video(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.meipai.com",
            "Referer": "http://www.meipai.com/"
        }
        pattern = re.compile('data-video="(.*?)"', re.S)
        pattern2 = re.compile('<meta name="description" content="(.*?)"', re.S)
        try:
            response = self.session.get(url=self.url, headers=headers, timeout=10)
            if response.status_code == 200:
                video_bs64 = re.findall(pattern, response.text)[0]
                title = re.findall(pattern2, response.text)[0]
                video_url = self.ctx.call("getmp4", video_bs64)
                info = {
                    "title": title,
                    "video": "https:"+video_url
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
"""


# 方法二
class MeiPai(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def getHex(self, a):
        hex_1 = a[:4][::-1]
        str_1 = a[4:]
        return str_1, hex_1

    def getDec(self, a):
        b = str(int(a, 16))
        c = list(b[:2])
        d = list(b[2:])
        return c, d

    def substr(self, a, b):
        k = int(b[0])
        c = a[:k]
        d = a[k:k + int(b[1])]
        temp = a[int(b[0]):].replace(d, "")
        result = c + temp
        return result

    def getPos(self, a, b):
        b[0] = len(a) - int(b[0]) - int(b[1])
        return b

    def get_video(self):
        # 预处理视频url地址
        pattern = re.compile(r'(http[s]?://[^\s]+)', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        # 定义全局浏览器标识符
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/84.0.4147.125 Safari/537.36 "

        headers = {
            "User-Agent": USER_AGENT,
            "Upgrade-Insecure-Requests": "1",
            "Host": "www.meipai.com",
            "Referer": "http://www.meipai.com/"
        }
        pattern = re.compile('data-video="(.*?)"', re.S)
        pattern2 = re.compile('<meta name="description" content="(.*?)"', re.S)
        try:
            response = self.session.get(url=deal_url, headers=headers, timeout=10)
            if response.status_code == 200:
                video_bs64 = re.findall(pattern, response.text)[0]
                title = re.findall(pattern2, response.text)[0]
                str1, hex1 = self.getHex(video_bs64)
                pre, tail = self.getDec(hex1)
                d = self.substr(str1, pre)
                kk = self.substr(d, self.getPos(d, tail))
                a = base64.b64decode(kk)
                base_url = "https:" + a.decode('utf-8')
                # 获取第一次重定向后的简化url
                headers = {
                    "Host": "mvvideo10.meitudata.com",
                    "Range": "bytes=0-",
                    "Referer": deal_url,
                    "User-Agent": USER_AGENT,
                }
                result = self.session.get(url=base_url, headers=headers, timeout=10)
                redirect_url = result.url

                # 获取第二次重定向后的简化url
                # 修改headers参数
                headers["Host"] = "cracl.meitubase.com"
                collection = self.session.get(url=redirect_url, headers=headers, timeout=10)
                redirect_url = collection.url

                info = {
                    "title": title,
                    "video": redirect_url,
                    "tips": "短视频无水印地址具有时效性，请及时保存，失效请重新获取"
                }
                return json.dumps(info, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    # meiPai = MeiPai("无水印 https://www.meipai.com/media/6815882149457056192")
    meiPai = MeiPai("有水印 https://www.meipai.com/media/6810586071534947553")
    print(meiPai.get_video())