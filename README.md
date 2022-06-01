# SSA
**学习通座位签到、预约、退座、暂离等等**

> 现在，你可以关注微信公众号“**杜恩**”或者搜索微信号“**heydoone**”更加快捷地使用接口的功能。
> <br>**不同学校的数据格式有些许的不同，可以在Issues提交你的问题，我会尽力解决的。**

# 功能接口将于6月5日前回归

新特性
* 功能与参数不变，有过一次请求过后响应更快。
* 验证码自助识别接口上线，将支持4位纯数字验证码，成功率约为99.2%。

验证码深度学习感谢以下项目的支持：

* **dee1024 & kenvifire：https://github.com/dee1024/pytorch-captcha-recognition**
* **PJDong：https://github.com/pprp/captcha_identify.pytorch**

## 目录

* <a href="#p3"><font size=2 color=#00f>接口更新日志</font></a><br>
* <a href="#pgjj"><font size=2 color=#00f>苹果捷径简单教程</font></a><br>

### 部分功能已经开通接口（<a href="#pgjj" color=#00f>苹果捷径使用方法</a>）

#### 签到

``` python
 # 请求地址:https://o.nvidia.fun:12345/sign
 # 请求方法:post
 # 请求参数:
{
    "phonenums": "手机号",
    "key":"密码"
}

 # response
{
    "msg": "不在签到时间内无法签到",
    "value": "True"
}
```

#### 离开、退座和取消

* 使用方法与签到一致，离开、退座和取消分别把url上的"sign"替换成"leave"、"signback"和"cancel"即可~

## <a id="pgjj">苹果捷径简单教程</a>

* 从url获取内容，url填上你要请求的地址，请求方式选择post，添加两个文本值，详细看下方的请求参数。
* 获取字典值，获取"msg"的值
* 显示提醒，将msg的值显示在弹窗。
