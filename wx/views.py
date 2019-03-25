import hashlib
import pytz
import requests
from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import wx_secrets
from . import models
from .message import WxMessageSender
from .access_token import get_pub_access_token

APPID = wx_secrets.WX_APPID
CHINA_TIMEZONE = pytz.timezone('Asia/Shanghai')


def login(request):
    """
    登陆视图，如果没有关注微信，那么跳转到关注页面
    :param request:
    :return:
    """
    if request.method == "POST":
        login_name = request.POST.get('loginname')
        password = request.POST.get('password')
        is_remember = request.POST.get('session_2weeks', None)
        try:
            user = models.Users.objects.get(loginname=login_name, password=password)
            # 使用会话记住用户登陆状态
            if 'username' in request.session:  # 只对存在登陆的会话进行flush或cycle_key
                if request.session['uid'] != user.uid:  # 如果会话中的用户就是当前进行登陆的用户那么进行cycle_key否则flush
                    request.session.flush()
                else:
                    request.session.cycle_key()  # 也会删除已存在的会话，但是会暂存老会话的数据，然后放入新会话中。
            if not is_remember:
                print('-->', "浏览器失效后session失效")
                request.session.set_expiry(0)  # 设置为关闭浏览器session失效。
            request.session['username'] = user.loginname
            request.session['uid'] = user.uid
            if user.wx_openid:
                return HttpResponse('He! Welcome! Our Gold!')
            return redirect(to=reverse('wx:bind_wx'))  # 进入绑定页面
        except ObjectDoesNotExist as e:
            return HttpResponse('用户名或密码错误！')

    return render(request, 'wx/login.html')


def wx_check(request):
    """
    微信公众平台：
        通过GET方式发送验证请求；
        通过POST方式发送用户消息和事件（如用户关注了微信）

    :param request:
    :return:
    """
    if request.method == "GET":
        data = request.GET.dict()
        if not data:
            return HttpResponse('hello wx!')
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = wx_secrets.OUR_TOKEN

        # 下面是签名验证
        tmp_list = [token, timestamp, nonce]
        print('tmp_list 排序前', tmp_list)

        tmp_list.sort()  # 微信要求就是要对这三个值列表排序

        print('tmp_list 排序后', tmp_list)

        sha1_obj = hashlib.sha1()
        sha1_obj.update(''.join(tmp_list).encode('utf-8'))
        if signature == sha1_obj.hexdigest():  # 验证成功放回echostr
            return HttpResponse(echostr)
        else:
            return HttpResponse('')
    elif request.method == 'POST':
        return HttpResponse('')
    else:
        return HttpResponse('')


def bind_wx(request):
    """
    绑定微信公众号，步骤引导页面
    :param request:
    :return:
    """
    return render(request, 'wx/bind_wx.html', {})


def get_authorized_url(request):
    """
    返回给用户进行授权操作的url地址。
    appid
    redirect_uri
    response_type
    scope
    state  --> 是重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节。用于与返回的code绑定。因为只有绑定了相关信息，
    才知道这个授权code绑定的信息（如用户信息）
    :param request:
    :return:
    """
    ret = {
        'code': 1000,
        'data': None
    }
    oauth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}#wechat_redirect"
    oauth_url = oauth_url.format(appid=APPID,
                                 redirect_uri="http://47.112.3.165" + reverse('wx:callback_bind_wx'),
                                 state=request.session.get('uid'))  # 回调地址必须在微信公众平台设置白名单
    ret['data'] = oauth_url
    print(oauth_url)
    return JsonResponse(ret)


def to_bind_wx(request):  # 获取到授权码后，访问微信开发平台获取OpenID
    code = request.GET.get('code')
    state = request.GET.get('state')

    user = models.Users.objects.filter(uid=state).first()

    if user.wx_openid:  # 从这里判定请求是否重复处理
        return HttpResponse('授权成功！')

    wx_api_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    result = requests.get(url=wx_api_url, params={'appid': APPID,
                                                  'secret': wx_secrets.WX_APPSECRET,
                                                  'code': code,
                                                  'grant_type': 'authorization_code'}).json()
    print(result)

    # 由于从微信请求该callback视图，会从微信或者微信代理发送多个请求，而我们的demo环境使用的是django的开发环境，所以不能并发处理多个请求。
    # 所以，这里对于多个同样的请求，由于是排队处理，即一个请求到响应完成，才会进行下一个请求的处理，所以按照这种请求处理模式，我们可以对多个同样
    # 的请求，做出判定，如果先到的请求已经处理，那么后续请求直接返回成功或失败，通过判定wx_openid是否已存在。
    # 虽然这种方式不适合生产，因为生产请求处理时并发的
    # result中包含了code授权证书对了的用户的信息，通。过code授权证书，可以拿到一个用户身份的access_token，这个access_tokne的权限是有限制

    try:
        openid = result['openid']
        user.wx_openid = openid
        user.save()
    except KeyError as e:
        print(e)
        return HttpResponse('授权失败，请重新扫码绑定！')
    else:
        sender = WxMessageSender(access_token=get_pub_access_token())
        # sender.csend(openid, 'Welcome!')

        sender.tsend({"touser": openid,
                      "template_id": "l0YWmbUvpLkDDTzeliSmee7-lFjjvZTEnySh1xkviG4",
                      "topcolor": "#FF0000",
                      "data": {
                          "datatime": {
                              "value": datetime.now(tz=CHINA_TIMEZONE).strftime("%Y-%m-%d"),
                              "color": "#173177"
                          },
                          "welcome": {
                              "value": "Welcome to my 测试号",
                              "color": "#173177"
                          }
                      }})
        return HttpResponse('授权成功，绑定成功')

# Create your views here.
