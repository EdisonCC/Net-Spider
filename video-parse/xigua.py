# -*- coding:utf-8 -*-
import re
import json
import base64
import requests
from pyquery import PyQuery as pq

"""
目标网站：西瓜视频
目标url：APP分享链接或web网页url
注意点：西瓜视频与哔哩哔哩都将音视频分割开了，用户只有使用剪辑软件自己拼接

update：2021-04-26
- 因为本人的技术比较拙劣，至今还没有找到音视频合一的无水印视频url
- 新版的api经过多次测试是需要携带cookie的，不存在cookie是无法获取数据的
- cookie并不是你登录后的cookie，你只需要任意打开一个西瓜🍉视频，在开发者模式下获取cookie
"""


class XiGua(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36 ",
            "cookie": 'wafid=aa79e1cd-16dc-421b-b94d-b20a5ebfe91c; wafid.sig=D1-hFWUnCB8JJJTV-R1e_Cdx9uI; '
                      '_ga=GA1.2.1690086969.1589782861; tt_webid=6865999761311827469; '
                      '__ac_nonce=060860ee900a3c46c139c; '
                      '__ac_signature=_02B4Z6wo00f01BqANnQAAIDDqnHav4zlIoQaoTLAAGYs20; '
                      'ttcid=f76179215341423fa72abd8cab05464915; MONITOR_WEB_ID=251a33dc-3fa9-413d-b16f-ea312209737e; '
                      'ttwid=1|gG2sxNEtarKxMKxuCZDzAK7r5j_05sBv8Nd-5HXNUhY|1619398378'
                      '|501f3788898a34f2c2a210c982bc82b2a22f0e365b65d7c2ff3ba9ce44be6b50; ixigua-a-s=0; '
                      'Hm_lvt_db8ae92f7b33b6596893cdf8c004a1a2=1619398389; '
                      'Hm_lpvt_db8ae92f7b33b6596893cdf8c004a1a2=1619398389; _gid=GA1.2.519205731.1619398389; '
                      '_tea_utm_cache_2285={"utm_source":"copy_link","utm_medium":"android",'
                      '"utm_campaign":"client_share"} '
        }
        try:
            response = self.session.get(url=deal_url, headers=headers, timeout=10)
            if response.status_code == 200:
                try:
                    html = pq(str(response.text))
                    doc = html("#SSR_HYDRATED_DATA").text()
                    # 用于处理js语法中的特定undefined关键字
                    doc = doc.replace("window._SSR_HYDRATED_DATA=", "").replace("undefined", '4396').strip()
                    # 处理特殊字符,并字典化
                    doc = json.loads(doc.encode('raw_unicode_escape').decode())
                    result = doc["anyVideo"]["gidInformation"]["packerData"]["video"]
                    cover = doc["anyVideo"]["gidInformation"]["packerData"]["pSeries"]["firstVideo"]["middle_image"]["url"]
                    # 获取标题
                    title = result["title"]
                    # 获取音视频合一的视频，但有水印存在
                    wm_video_url = result["videoResource"]["normal"]["video_list"].get("video_4", "video_1").get("main_url", "backup_url_1")
                    quality = result["videoResource"]["dash"]["dynamic_video"]["dynamic_video_list"][-1]["definition"]
                    # 获取无水印，但音视频分割的视频地址
                    video_url = result["videoResource"]["dash"]["dynamic_video"]["dynamic_video_list"][-1].get("main_url", "backup_url_1")
                    audio_url = result["videoResource"]["dash"]["dynamic_video"]["dynamic_audio_list"][-1].get("main_url", "backup_url_1")
                    info = {
                        "title": title,
                        "quality": quality,
                        "cover": cover,
                        "video_url": base64.b64decode(video_url).decode("utf-8"),
                        "audio_url": base64.b64decode(audio_url).decode("utf-8"),
                        "wm_video_url": base64.b64decode(wm_video_url).decode("utf-8"),
                        "description": "本api会选择视频清晰度最高的视频；西瓜视频的音视频是分离开的，请搭配使用剪辑软件拼接音视频源（wm_video_url是音视频合一的，但存在水印）"
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    xigua = XiGua(
        "https://www.ixigua.com/6837727489259733518/?app=video_article&timestamp=1602058436&utm_source=copy_link"
        "&utm_medium=android&utm_campaign=client_share")
    print(xigua.get_video())
