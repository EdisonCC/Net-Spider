# -*- coding:utf-8 -*-

"""
聚合索引：
    - 把短视频去水印的接口聚合一起，输入一个url地址就可以自动识别是哪个平台的地址，不用手动选择
    - 有可能会因为域名的改变而无法正确解析到对应的接口
"""

def allinone(url):
    res = ''
    if 'm.acfun.cn' in url:
        import acfun
        res = acfun.AcFun(url)
    elif 'm.hanyuhl.com' in url:
        import before
        res = before.Before(url)
    elif 'bilibili.com' in url:
        import bilibili
        res = bilibili.BiLiPhone(url)
    elif 'h5.hibixin.com' in url:
        import bixin
        res = bixin.BiXin(url)
    elif 'www.xinpianchang.com' in url:
        import changku
        res = changku.ChangKuVideo(url)
    elif 'p.doupai.cc' in url:
        import doupai
        res = doupai.DouPai(url)
    elif 'v.douyin.com' in url:
        import douyin2_parse
        res = douyin2_parse.DouYin2(url)
    elif 'haokan.baidu.com' in url:
        import haokan
        res = haokan.HaoKan(url)
    elif 'share.huoshan.com' in url:
        import huoshan_parse
        res = huoshan_parse.HuoShan(url)
    elif 'v.huya.com' in url:
        import huya
        res = huya.HuYa(url)
    elif 'www.eyepetizer.net' in url:
        import kaiyan_parse
        res = kaiyan_parse.OpenEye(url)
    elif 'video.kuaishou.com' in url:
        import kuaishou
        res = kuaishou.KuaiShou(url)
    elif 'www.17kuxiu.com' in url:
        import kuxiu
        res = kuxiu.KuXiu(url)
    elif 'm.oasis.weibo.cn' in url:
        import lvzhou
        res = lvzhou.LvZhou(url)
    elif 'n.miaopai.com' in url:
        import miaopai_parse
        res = miaopai_parse.MiaoPai(url)
    elif 'm.immomo.com' in url:
        import momo
        res = momo.MoMo(url)
    elif 'www.pearvideo.com' in url:
        import pear
        res = pear.PearVideo(url)
    elif 'h5.ippzone.com' in url:
        import pipi_funny
        res = pipi_funny.PiPiFunny(url)
    elif 'h5.pipix.com' in url:
        import pipixia
        res = pipixia.PiPiXia(url)
    elif 'pornhub.com' in url:
        import pornhub
        res = pornhub.PornHub(url)
    elif 'quanmin.baidu.com' in url:
        import quanmin
        res = quanmin.QuanMin(url)
    elif 'qq.com' in url:
        import quanmin_kge
        res = quanmin_kge.KGe(url)
    elif 'xhslink.com' in url:
        import xhs_parse
        res = xhs_parse.XiaoHongShu(url)
    elif 'mobile.xiaokaxiu.com' in url:
        import xiaokaxiu_parse
        res = xiaokaxiu_parse.XiaoKaXiu(url)
    elif 'www.ixigua.com' in url:
        import xigua
        res = xigua.XiGua(url)
    elif 'share.izuiyou.com' in url:
        import zuiyou
        res = zuiyou.ZuiYou(url)
    elif 'v.6.cn' in url:
        import sixroom
        res = sixroom.sixRoom(url)
    elif 'm.vuevideo.net' in url:
        import vue_parse
        res = vue_parse.Vue(url)
    elif 'weibo.com' in url:
        import weibo
        res = weibo.WeiBo(url)
    elif 'h5.weishi.qq.com' in url:
        import weishi_parse
        res = weishi_parse.WeiShi(url)
    else:
        return '未匹配到相关接口'
    if res != '':
        # print(res.get_video())
        return res.get_video()


if __name__ == '__main__':
    print(allinone('https://www.bilibili.com/video/BV1T54y1a7yc'))
