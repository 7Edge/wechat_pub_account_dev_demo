# wechat_pub_account_dev_demo
微信公众号开发demo

## 主要实现功能
1. openid绑定站内号;
2. 推送业务消息;
3. 推送自定义消息和模板消息.
4. redis缓存access_token

## 公众号
> 由于个人订阅号不能认证，接口调用权限有限，所以使用微信公众号提供的测试公众号进行demo开发。

- 测试公众号使用地址:https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login 打开使用自己的微信扫码登陆即可，
微信可以自动将测试公众号注册号，只需要根据页面提示就可以使用测试微信公众号，且接口使用权限已经开通。

### 接入微信公众号开发平台
#### 服务器配置
1. 我方服务器URL，用户接受微信消息和事件的接口
2. Token，这个用于生成签名。
3. EncodingAESKey 消息体加解密密钥(测试号不用设置)

### 完成功能概述

#### 01.响应微信公众号平台发送的验证消息
1. 请求方式GET, 请求发送到填写的URL地址
2. GET携带的参数：signature 微信加密签名; timestamp 时间戳; nonce 随机数; echostr 随机字符串；
3. 验证消息目的主要就是验证签名就可以了，因为只有微信和自己知道token的值，所以经过hash即可进行签名验证。
4. 在wx.views.wx_check视图进行完整验证。（注意有时候检测请求是post请求，注意将视图csrf_exempt装饰，避免csrf中间件拒绝）

#### 02. 站内号登陆

#### 03. 站内号绑定用户微信号，推送业务消息


### 运行demo
####  依赖环境
- 项目运行利用python虚拟环境,使用pipenv on python3 环境
    1. pipenv install 
    2. pipenv shell
- 数据库
    1. settings.py中设置好数据库选项（我这里使用的是mysql，其它都可以）
    2. 在虚拟环境下进行：python manage.py makemigrations
    3. python manage.py migrate
- 配置redis缓存：
    1. 安装启动redis
    2. settings.py 中修改redis服务的地址和端口，有密码设置密码
- 启动项目，在开发环境：
    1. python manage.py runserver 0.0.0.0:80

- 访问/wx/login/
 
