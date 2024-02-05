# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：小红书
目标url：APP短视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：http://xhslink.com/xvxMJ
    2. url重定向到真实跳转地址：简化后.,https://www.xiaohongshu.com/discovery/item/5f77dbcf000000000100491c...
    3. As of 2020-11-04 小红书更新，不再提供无水印接口。且请求头必须携带cookie，才能获取数据
更新：2024-2-5 直接获取originVideoKey，进而得到无水印地址
"""


class XiaoHongShu(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        try:
            # 处理url
            pattern = re.compile(r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])+',re.S)
            deal_url = re.findall(pattern, self.url)[0]

            # 获取重定向后的简化url
            response = self.session.get(url=deal_url, headers=headers, allow_redirects=False, timeout=10)
            base_url = response.headers.get("Location")

            result = self.session.get(url=base_url, headers=headers, timeout=10)
            if result.status_code == 200:
                try:
                    origin_video_key = re.findall(r'"originVideoKey":"(.*?)"', result.text)[0]
                    origin_video_key = origin_video_key.encode('utf-8').decode('unicode_escape')
                    cover = re.findall(r'style="background-image:url\((.*?)\)', result.text)[0]
                    description = re.findall(r'name="description" content="(.*?)"', result.text)[0]
                    info = {
                        "description": description,
                        "cover": "https:" + cover,
                        "url": "http://sns-video-hw.xhscdn.com/" + origin_video_key
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    redbook = XiaoHongShu("53 【十分硬核的十部战争枪战电影推荐 - 七日放映厅 | 小红书 - 你的生活指南】 😆 OpjvLg4SuAwIPQo 😆 http://xhslink.com/3bqx3A")
    print(redbook.get_video())