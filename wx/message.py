#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: message
# Date: 3/21/2019
"""
发送微信消息
"""
import requests
import json

import wx_secrets


class BaseMessageSender:

    def send(self, to_who, message):
        """
        发送message消息给to_who
        :param to_who:
        :param message:
        :return:
        """
        raise NotImplementedError("subclass of BaseMessageSender must provide a send() method")


class WxMessageSender(object):
    """
    发送微信消息
    """
    custom_url = wx_secrets.SMS_CUSTOM_URL
    template_url = wx_secrets.SMS_TEMPLATE_URL

    def __init__(self, access_token):
        self.access_token = access_token

    def csend(self, openid, content):
        body = {
            'touser': openid,
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }

        body = bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')

        result = requests.post(url=self.custom_url,
                               params={
                                   'access_token': self.access_token
                               },
                               data=body).json()
        print(result)
        return result

    def tsend(self, template):
        result = requests.post(url=self.template_url,
                               params={
                                   'access_token': self.access_token
                               },
                               json=template).json()
        print('模板消息响应：', result)
        return result


if __name__ == '__main__':
    pass
