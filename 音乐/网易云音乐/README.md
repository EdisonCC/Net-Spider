## 网易云音乐

### 1、参考文章

+ [python的AES-CBC加密](https://zhuanlan.zhihu.com/p/184968023)

### 2、解析原理
核心js文件：https://s3.music.126.net/web/s/core_218ed265fbaa5bb4f64fdbcaaefef8ba.js

逆向入口(格式化之后在8015行左右)
``` javascript
var v = encrypt.asrsea(JSON.stringify(r), enk.emj2code(["流泪", "强"]), enk.BASE_CODE, enk.emj2code(["爱心", "女孩", "惊恐", "大笑"]));
return a.body = obj2query({
    params: v.encText,
    encSecKey: v.encSecKey
}),
```
#### params
追踪之后可以发现

**params**参数也就是**v.encText**是通过将
```
{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"音乐名","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
```
经过*两次***AES CBC**加密得到的

关键代码如下
``` javascript
function b(a, b) {
	var c = CryptoJS.enc.Utf8.parse(b),
		d = CryptoJS.enc.Utf8.parse("0102030405060708"),
        e = CryptoJS.enc.Utf8.parse(a),
        f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
    return f.toString()
    }
```

#### encSecKey
encSecKey的获取就有亿点点恶心了。。。

关键代码(很短)：
``` javascript
function c(a, b, c) {
    var d, e;
    return setMaxDigits(131), d = new RSAKeyPair(b, "", c), e = encryptedString(d, a)
    }
```
然而，当你欢喜地把这段代码扔到execjs里执行，你就会发现*根本执行不了*

原因就出在**RSAKeyPair**

这个函数依赖[BigInt.js](http://www.ohdave.com/rsa/BigInt.js)和[Barrett.js](http://www.ohdave.com/rsa/Barrett.js)(找到我崩溃...)

将这三部分代码合并，就成了[crack.js](./crack.js)