# -*- coding:utf-8 -*-
import re
import json
import requests

"""
目标APP：皮皮虾
目标url：APP短视频分享链接
爬取思路：
    1. 通过APP里的分享获取视频url：https://h5.pipix.com/s/JAtW8Yg/
    2. url重定向到真实跳转地址：简化后.,https://h5.pipix.com/item/6869230768778909965
    3. 获取重定向后的url的item_id,携带其发送get请求
    4. As of 10/20/2020, 皮皮虾app更新了接口不再暴露无水印视频地址
奇怪点：
    1. 任意分享的视频链接如下：
       - https://h5.pipix.com/s/3asShh（✅）
       - https://h5.pipix.com/s/JRjEVyT（✖）
       - https://h5.pipix.com/s/JAtW8Yg（✖）
       - https://h5.pipix.com/s/rR5Ppu（✅）
    2. 发现有些视频链接，获取访问结果的json中的“comment”字段里居然藏有无水印的视频url
    3. 有些分享链接的comment字段为空数组，有些又有值。想通过app分享链接百分百拿到无水印视频url感觉有点困难，除非知道内部视频数据api

2021-03-22 更新：
    接上：终于知道为什么这些视频分享链接有些是可以获取，有些无法获取，原因在于其【视频是否有评论】，我们的无水印解析基础是通过评论里获取的
    皮皮虾的短视频【推荐】板块是每次post请求，返回6条数据，滑动6个视频后会重新请求，根据这个api好像不能查询某个具体的视频，
        于是我就点击详细页，发现了评论的api中找到了这个无水印的短视频URL。美中不足的是：假如某个视频是没有评论的，返回的就是一个空数组
"""


class PiPiXia(object):
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def get_vid(self):
        """
        获取视频id
        :return: String
        """
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36"
        }
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        deal_url = re.findall(pattern, self.url)[0]
        response = self.session.get(url=deal_url, headers=headers, timeout=10)
        # 获取视频id
        pattern = re.compile("item/(\d+)?", re.S)
        video_id = re.findall(pattern, str(response.url).strip())[0]
        return video_id

    def get_video(self, cell_id):
        """
        获取皮皮虾无水印视频链接方法一（前提是该视频有评论）
        :param cell_id: 分享视频的唯一标识
        :return: String
        """
        share_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.193 Safari/537.36 "
        }
        try:
            # get请求视频地址
            api = "https://h5.pipix.com/bds/webapi/item/detail/?item_id={}&source=share".format(cell_id)
            result = self.session.get(url=api, headers=share_headers, timeout=10)
            if result.status_code == 200:
                try:
                    res = result.json()
                    title = res["data"]["item"]['content']
                    # 判断comments是否为空
                    if len(res["data"]["item"]['comments']) > 0:
                        # comment里面才是真正的无水印视频地址
                        url = res["data"]["item"]['comments'][0]['item']['video']['video_high']['url_list'][0]['url']
                    else:
                        # 去有水印的视频地址
                        url = res["data"]["item"]["video"]["video_download"]["url_list"][0]["url"]
                    name = res["data"]["item"]["author"]["name"]
                    cover = res["data"]["item"]["cover"]["url_list"][0]["url"]
                    description = res["data"]["item"]["author"]["description"]
                    info = {
                        "title": title,
                        "name": name,
                        "description": description,
                        "cover": cover,
                        "video_url": url
                    }
                    return json.dumps(info, ensure_ascii=False)
                except Exception as e:
                    return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
            else:
                return json.dumps({"info": "暂无相关数据，请检查相关数据："}, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)

    def get_video2(self, cell_id):
        """
        获取皮皮虾无水印视频链接方法二（前提是该视频有评论）
        :param cell_id: 分享视频的唯一标识
        :return: String
        """
        params = {
            'cell_id': cell_id,
            'aid': '1319',
            'app_name': 'super',
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/85.0.4183.102 Safari/537.36"
        }
        url = "https://i-lq.snssdk.com/bds/cell/cell_comment/"
        response = self.session.get(url=url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                rsp = response.json()
                if len(rsp["data"]["cell_comments"]) > 0:
                    row = rsp["data"]["cell_comments"][0]
                    author = row["comment_info"]["item"]["author"]["name"]
                    content = row["comment_info"]["item"]["content"]
                    cover = row["comment_info"]["item"]["cover"]["url_list"][0]["url"]
                    video_url = row["comment_info"]["item"]["video"]["video_high"]["url_list"][0]["url"]
                    info = {
                        "name": author,
                        "description": content,
                        "cover": cover,
                        "video_url": video_url
                    }
                    return json.dumps(info, ensure_ascii=False)
                else:
                    return json.dumps({"info": "当前仅支持解析带有评论的皮皮虾分享视频"}, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"info": "暂无相关数据，请检查相关数据：" + str(e)}, ensure_ascii=False)
        else:
            return json.dumps({"info": response.status_code}, ensure_ascii=False)


if __name__ == '__main__':
    letter = """
    尊敬的用户：
        当前暂时仅支持解析【带有评论的皮皮虾分享视频】
        若【真的真的真的】想将漂亮小姐姐的视频带回家，那就给小姐姐的视频留言吧！
    """
    print(letter)
    pi_pi = PiPiXia("Rosé发布了一篇皮皮虾视频，快来看吧！😆 https://h5.pipix.com/s/3asShh ，复制本条信息")
    # 获取视频唯一标识cell_id
    vid = pi_pi.get_vid()
    # content = pi_pi.get_video(cell_id=vid)
    content = pi_pi.get_video2(cell_id=vid)
    print(content)