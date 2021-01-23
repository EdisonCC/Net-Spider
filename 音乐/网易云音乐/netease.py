# -*- coding:utf-8 -*-
import json
import base64
import execjs
import random
import requests
from Crypto.Cipher import AES


def random_generate(number):
    b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    c = ""
    for i in range(number):
        c += b[int(random.random() * len(b))]
    return c


class Netease:
    """
    Purpose: 网易云音乐爬取/解析
    Author: Ravizhan
    Github: https://github.com/ravizhan

    + 大概的解析流程：
        1. 通过两次AES CBC加密，获取params参数
        2. 调用execjs执行加密js，获取encSecKey参数
        3. 整合参数，发送post请求

    + 参数说明：
        + p:随机生成16位的字符串
        + key:固定的AES密钥
        + iv:固定的AES偏移量
        + id:网易云音乐每首歌对应的唯一id 例:https://music.163.com/#/song?id=355992

    + 注:AES加密部分参考自 https://zhuanlan.zhihu.com/p/184968023
        之前试了很多方法都实现不了AES CBC加密，本来是调用在线加密api进行加密的，但是效率过于低下
        直到看到了那篇文章.....
    """

    def __init__(self, key='0CoJUm6Qyw8W8jud', iv='0102030405060708'):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')
        # 随机生成16位的字符串
        # 貌似不用每次都重新生成(管他呢)
        self.p = random_generate(16)

    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        return text + padding_text

    def aes_encrypt(self, content, key='0CoJUm6Qyw8W8jud'):
        """
        AES加密
        """
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def get_params(self, n):
        # 进行第一次AES CBC加密
        # key=0CoJUm6Qyw8W8jud iv=0102030405060708
        # key和iv都是定值
        string = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}' % n
        res = self.aes_encrypt(string)
        # 进行第二次加密
        # 此处的key为一开始随机生成的(固定的貌似也行)，iv还是0102030405060708
        res = self.aes_encrypt(res, self.p)
        return res

    def get_encSecKey(self):
        # 用几百行看不懂的js生成encSecKey....
        with open('crack.js', 'r')as f:
            code = f.read()
        js = execjs.compile(code)
        enc = js.call('c', self.p, '010001',
                      '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7')
        return enc

    def search(self, params, enc):
        name_list, id_list = [], []
        # 组合参数并post请求
        data = {
            'params': params,
            'encSecKey': enc
        }
        # print(data)
        text = requests.post('https://music.163.com/weapi/cloudsearch/get/web?csrf_token=', data=data).text
        res = json.loads(text)
        # 解析返回的json
        for i in range(0, 20):
            name_list.append(res['result']['songs'][i]['name'])
            id_list.append(res['result']['songs'][i]['id'])
        return name_list, id_list

    def download_url(self, id):
        # 此处获取params的方法与get_params函数相同
        string = '{"ids":"[%s]","level":"standard","encodeType":"aac","csrf_token":""}' % id
        params = self.aes_encrypt(string)
        params = self.aes_encrypt(params, self.p)
        enc = self.get_encSecKey()
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        text = requests.post(url, data={'params': params, 'encSecKey': enc}, headers=headers).text
        res = json.loads(text)
        return res['data'][0]['url']


if __name__ == '__main__':
    name = input('请输入要搜索的歌曲:')
    wy = Netease()
    name_list, id_list = wy.search(wy.get_params(name), wy.get_encSecKey())
    print(name_list, id_list)