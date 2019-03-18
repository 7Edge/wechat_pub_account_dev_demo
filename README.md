# wechat_pub_account_dev_demo
微信公众号开发demo

## 主要实现功能
1. openid绑定站内号;
2. 推送业务消息;
3. 推送自定义消息和模板消息.

## 公众号
> 由于个人订阅号不能认证，接口调用权限有限，所以使用微信公众号提供的测试公众号进行demo开发。

- 测试公众号使用地址:https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login 打开使用自己的微信扫码登陆即可，
微信可以自动将测试公众号注册号，只需要根据页面提示就可以使用测试微信公众号，且接口使用权限已经开通。

### 接入微信公众号开发平台
#### 服务器配置
1. 我方服务器URL，用户接受微信消息和事件的接口
2. Token，这个用于生成签名。
3. EncodingAESKey 消息体加解密密钥

#### 微信公众号平台发送的验证消息
1. 请求方式GET, 请求发送到填写的URL地址
2. GET携带的参数：signature 微信加密签名; timestamp 时间戳; nonce 随机数; echostr 随机字符串；
3. 
 
