import hashlib

from django.shortcuts import render, HttpResponse

import wx_secrets


def wx_check(request):
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

# Create your views here.
