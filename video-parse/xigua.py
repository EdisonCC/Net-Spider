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

update: 2023-06-23
- 新增音视频合一的无水印视频解析
- 新版api依旧需要cookie
"""


class XiGua(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_video(self):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        headers = {
            "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36''',
            "cookie": '''__ac_nonce=06495214000a2485c177; __ac_signature=_02B4Z6wo00f01JD4UgQAAIDAEPqoRhFZyPyQ2FaAAECv8e; csrf_session_id=250ab1295701df7121466ac7e69f663d; support_webp=true; support_avif=true; ixigua-a-s=1; ttcid=4df1fc731c324052812992579ef3ab5314; msToken=AZm8m-J4RHLTaQGJlCn2TL1fuSMIk-cbCIEbkMoZp6f2NW42elghJGs-d89uTa7B7oxAMJ6T-b7X1yo5slETItfRnoqjkX_ljPZdm4nM4nQFFRMo2ka5r_wn5SiYLQ==; tt_scid=U3SUlIdh7eZjZnQaipHEvKA9gagvBo9p7NRW63B1l3rm4ugaSpB0itoYHp.gtNEI7cdd; ttwid=1%7CZ4W7EofKKAG94xPgvf4SRa_PoXmW7DuACXXkCHL2er8%7C1687495018%7Ce0d81d84da4baf97a6dbb028dae3eb2f7faf65d41b827cfe565d2de34fabafa5'''
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
                    cover = result["poster_url"]
                    # 获取标题
                    title = result["title"]
                    # # 获取音视频合一的视频，但有水印存在
                    # wm_video_url = result["videoResource"]["normal"]["video_list"].get("video_4", "video_1").get("main_url", "backup_url_1")
                    # quality = result["videoResource"]["dash"]["dynamic_video"]["dynamic_video_list"][-1]["definition"]
                    # # 获取无水印，但音视频分割的视频地址
                    # video_url = result["videoResource"]["dash"]["dynamic_video"]["dynamic_video_list"][-1].get("main_url", "backup_url_1")
                    # audio_url = result["videoResource"]["dash"]["dynamic_video"]["dynamic_audio_list"][-1].get("main_url", "backup_url_1")
                    # info = {
                    #     "title": title,
                    #     "quality": quality,
                    #     "cover": cover,
                    #     "video_url": base64.b64decode(video_url).decode("utf-8"),
                    #     "audio_url": base64.b64decode(audio_url).decode("utf-8"),
                    #     "wm_video_url": base64.b64decode(wm_video_url).decode("utf-8"),
                    #     "description": "本api会选择视频清晰度最高的视频；西瓜视频的音视频是分离开的，请搭配使用剪辑软件拼接音视频源（wm_video_url是音视频合一的，但存在水印）"
                    # }
                    # 选择最高清晰度
                    definition = sorted(result["videoResource"]["normal"]["video_list"])[-1]
                    quality = result["videoResource"]["normal"]["video_list"][definition]["definition"]
                    # 无水印地址
                    video_url = result["videoResource"]["normal"]["video_list"][definition].get("main_url", "backup_url")
                    info = {
                        "title": title,
                        "quality": quality,
                        "cover": cover,
                        "video_url": base64.b64decode(video_url).decode("utf-8"),
                        "description": "本api会选择视频清晰度最高的视频;视频链接需添加refer:https://www.ixigua.com/才能正常访问"
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)


if __name__ == '__main__':
    xigua = XiGua("https://www.ixigua.com/7222107373476053562")
    print(xigua.get_video())
