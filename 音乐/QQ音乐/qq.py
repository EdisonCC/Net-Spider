import execjs
import requests
from urllib import parse
import json
'''
QQ音乐爬取/解析
作者:Ravizhan
'''
# 获取sign参数
def sign(a):
    #利用execjs模拟执行加密js，减少工作量，但效率较低
    js = execjs.compile('''
    var n = function() {
            if ("undefined" != typeof self)
                return self;
            if ("undefined" != typeof window)
                return window;
            if ("undefined" != typeof global)
                return global;
            throw new Error("unable to locate global object")
        }();
        n.__sign_hash_20200305 = function(n) {
            function l(n, t) {
                var o = (65535 & n) + (65535 & t);
                return (n >> 16) + (t >> 16) + (o >> 16) << 16 | 65535 & o
            }
            function r(n, t, o, e, u, p) {
                return l((i = l(l(t, n), l(e, p))) << (r = u) | i >>> 32 - r, o);
                var i, r
            }
            function g(n, t, o, e, u, p, i) {
                return r(t & o | ~t & e, n, t, u, p, i)
            }
            function a(n, t, o, e, u, p, i) {
                return r(t & e | o & ~e, n, t, u, p, i)
            }
            function s(n, t, o, e, u, p, i) {
                return r(t ^ o ^ e, n, t, u, p, i)
            }
            function v(n, t, o, e, u, p, i) {
                return r(o ^ (t | ~e), n, t, u, p, i)
            }
            function t(n) {
                return function(n) {
                    var t, o = "";
                    for (t = 0; t < 32 * n.length; t += 8)
                        o += String.fromCharCode(n[t >> 5] >>> t % 32 & 255);
                    return o
                }(function(n, t) {
                    n[t >> 5] |= 128 << t % 32,
                    n[14 + (t + 64 >>> 9 << 4)] = t;
                    var o, e, u, p, i, r = 1732584193, f = -271733879, h = -1732584194, c = 271733878;
                    for (o = 0; o < n.length; o += 16)
                        r = g(e = r, u = f, p = h, i = c, n[o], 7, -680876936),
                        c = g(c, r, f, h, n[o + 1], 12, -389564586),
                        h = g(h, c, r, f, n[o + 2], 17, 606105819),
                        f = g(f, h, c, r, n[o + 3], 22, -1044525330),
                        r = g(r, f, h, c, n[o + 4], 7, -176418897),
                        c = g(c, r, f, h, n[o + 5], 12, 1200080426),
                        h = g(h, c, r, f, n[o + 6], 17, -1473231341),
                        f = g(f, h, c, r, n[o + 7], 22, -45705983),
                        r = g(r, f, h, c, n[o + 8], 7, 1770035416),
                        c = g(c, r, f, h, n[o + 9], 12, -1958414417),
                        h = g(h, c, r, f, n[o + 10], 17, -42063),
                        f = g(f, h, c, r, n[o + 11], 22, -1990404162),
                        r = g(r, f, h, c, n[o + 12], 7, 1804603682),
                        c = g(c, r, f, h, n[o + 13], 12, -40341101),
                        h = g(h, c, r, f, n[o + 14], 17, -1502002290),
                        r = a(r, f = g(f, h, c, r, n[o + 15], 22, 1236535329), h, c, n[o + 1], 5, -165796510),
                        c = a(c, r, f, h, n[o + 6], 9, -1069501632),
                        h = a(h, c, r, f, n[o + 11], 14, 643717713),
                        f = a(f, h, c, r, n[o], 20, -373897302),
                        r = a(r, f, h, c, n[o + 5], 5, -701558691),
                        c = a(c, r, f, h, n[o + 10], 9, 38016083),
                        h = a(h, c, r, f, n[o + 15], 14, -660478335),
                        f = a(f, h, c, r, n[o + 4], 20, -405537848),
                        r = a(r, f, h, c, n[o + 9], 5, 568446438),
                        c = a(c, r, f, h, n[o + 14], 9, -1019803690),
                        h = a(h, c, r, f, n[o + 3], 14, -187363961),
                        f = a(f, h, c, r, n[o + 8], 20, 1163531501),
                        r = a(r, f, h, c, n[o + 13], 5, -1444681467),
                        c = a(c, r, f, h, n[o + 2], 9, -51403784),
                        h = a(h, c, r, f, n[o + 7], 14, 1735328473),
                        r = s(r, f = a(f, h, c, r, n[o + 12], 20, -1926607734), h, c, n[o + 5], 4, -378558),
                        c = s(c, r, f, h, n[o + 8], 11, -2022574463),
                        h = s(h, c, r, f, n[o + 11], 16, 1839030562),
                        f = s(f, h, c, r, n[o + 14], 23, -35309556),
                        r = s(r, f, h, c, n[o + 1], 4, -1530992060),
                        c = s(c, r, f, h, n[o + 4], 11, 1272893353),
                        h = s(h, c, r, f, n[o + 7], 16, -155497632),
                        f = s(f, h, c, r, n[o + 10], 23, -1094730640),
                        r = s(r, f, h, c, n[o + 13], 4, 681279174),
                        c = s(c, r, f, h, n[o], 11, -358537222),
                        h = s(h, c, r, f, n[o + 3], 16, -722521979),
                        f = s(f, h, c, r, n[o + 6], 23, 76029189),
                        r = s(r, f, h, c, n[o + 9], 4, -640364487),
                        c = s(c, r, f, h, n[o + 12], 11, -421815835),
                        h = s(h, c, r, f, n[o + 15], 16, 530742520),
                        r = v(r, f = s(f, h, c, r, n[o + 2], 23, -995338651), h, c, n[o], 6, -198630844),
                        c = v(c, r, f, h, n[o + 7], 10, 1126891415),
                        h = v(h, c, r, f, n[o + 14], 15, -1416354905),
                        f = v(f, h, c, r, n[o + 5], 21, -57434055),
                        r = v(r, f, h, c, n[o + 12], 6, 1700485571),
                        c = v(c, r, f, h, n[o + 3], 10, -1894986606),
                        h = v(h, c, r, f, n[o + 10], 15, -1051523),
                        f = v(f, h, c, r, n[o + 1], 21, -2054922799),
                        r = v(r, f, h, c, n[o + 8], 6, 1873313359),
                        c = v(c, r, f, h, n[o + 15], 10, -30611744),
                        h = v(h, c, r, f, n[o + 6], 15, -1560198380),
                        f = v(f, h, c, r, n[o + 13], 21, 1309151649),
                        r = v(r, f, h, c, n[o + 4], 6, -145523070),
                        c = v(c, r, f, h, n[o + 11], 10, -1120210379),
                        h = v(h, c, r, f, n[o + 2], 15, 718787259),
                        f = v(f, h, c, r, n[o + 9], 21, -343485551),
                        r = l(r, e),
                        f = l(f, u),
                        h = l(h, p),
                        c = l(c, i);
                    return [r, f, h, c]
                }(function(n) {
                    var t, o = [];
                    for (o[(n.length >> 2) - 1] = void 0,
                    t = 0; t < o.length; t += 1)
                        o[t] = 0;
                    for (t = 0; t < 8 * n.length; t += 8)
                        o[t >> 5] |= (255 & n.charCodeAt(t / 8)) << t % 32;
                    return o
                }(n), 8 * n.length))
            }
            function o(n) {
                return t(unescape(encodeURIComponent(n)))
            }
            return function(n) {
                var t, o, e = "0123456789abcdef", u = "";
                for (o = 0; o < n.length; o += 1)
                    t = n.charCodeAt(o),
                    u += e.charAt(t >>> 4 & 15) + e.charAt(15 & t);
                return u
            }(o(n))
        }
    function getSign(data) {
      let str = 'abcdefghijklmnopqrstuvwxyz0123456789';
      let count = Math.floor(Math.random() * 7 + 10);
      let sign = 'zza';
      for(let i = 0; i < count ; i++){
        sign += str[Math.floor(Math.random() * 36)];
      }
      sign += global.__sign_hash_20200305('CJBPACrRuNy7'+JSON.stringify(data));
      return sign
    }
    const data = {"comm":{"ct":24,"cv":0},"vip":{"module":"userInfo.VipQueryServer","method":"SRFVipQuery_V2","param":{"uin_list":["2876473037"]}},"base":{"module":"userInfo.BaseUserInfoServer","method":"get_user_baseinfo_v2","param":{"vec_uin":["2876473037"]}}}
    console.log(getSign(data))
    ''')
    return js.call('getSign', a)

# 获取下载地址
def getdownloadurl(song_mid):
    song_mid = song_mid.replace("'", "\"")
    # 此处的guid和uin都是每个账号唯一的
    # 这里用的是我自己的(非vip，没钱..)，无法下载vip歌曲，有vip账号的可以更换uin和guid试试
    sec = {
        "req": {
            "module": "CDN.SrfCdnDispatchServer",
            "method": "GetCdnDispatch",
            "param": {
                "guid": "5294554992",
                "calltype": 0,
                "userip": ""}},
        "req_0": {
            "module": "vkey.GetVkeyServer",
            "method": "CgiGetVkey",
            "param": {
                "guid": "5294554992",
                "songmid": [song_mid],
                "songtype": [0],
                "uin": "2876473037",
                "loginflag": 1,
                "platform": "20"}},
        "comm": {
            "uin": 2876473037,
            "format": "json",
            "ct": 24,
            "cv": 0}}
    params = '''{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"5294554992","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"5294554992","songmid":["%s"],"songtype":[0],"uin":"2876473037","loginflag":1,"platform":"20"}},"comm":{"uin":2876473037,"format":"json","ct":24,"cv":0}}''' % (
        song_mid)
    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?-=getplaysongvkey4888498303971036&g_tk=1810605017&sign=' + \
          sign(sec) + '&loginUin=1&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=' + parse.quote(params)
    text = requests.get(url).text
    text = json.loads(text)
    return [
        text['req_0']['data']['sip'][0] +
        text['req_0']['data']['midurlinfo'][0]['purl'],
        text['req_0']['data']['sip'][1] +
        text['req_0']['data']['midurlinfo'][0]['purl']]


def search(song_name):
    song_mid, song_url, song_res_name,singer = [], [], [], []
    text = requests.get(
        'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=10&format=json&w=' +
        song_name).text
    text = json.loads(text)
    for i in range(0, 10):
        song_mid.append(text['data']['song']['list'][i]['songmid'])
        singer.append(text['data']['song']['list'][i]['singer'][0]['name'])
        song_url.append('https://y.qq.com/n/yqq/song/' + song_mid[i] + '.html')
        song_res_name.append(text['data']['song']['list'][i]['songname'])
    return song_mid, song_url, song_res_name, singer


if __name__ == '__main__':
    song_name = input('请输入要搜索的歌曲名:')
    song_mid, song_url, song_res_name, singer = search(song_name)
    for i in range(0, len(song_res_name)):
        print('%d.歌曲名：%s  歌手：%s\n地址：%s' % (i + 1, song_res_name[i], singer[i], song_url[i]))
    choice = input('请选择一首[1~10]：')
    choice = int(choice) - 1
    print('下载地址1：' + getdownloadurl(song_mid[choice])[0])
    print('下载地址2：' + getdownloadurl(song_mid[choice])[1])
    input('按任意键退出')
