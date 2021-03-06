#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: access_token
# Date: 3/21/2019
"""
获取公众号访问接口的access_token,缓存到redis中，有效期设置为2个小时。命中者读取，没有命中则重新获取并存储
"""
import wx_secrets
import requests
from django_redis import get_redis_connection


def get_pub_access_token():
    redis_conn = get_redis_connection('default')
    if redis_conn.exists('zhangjiaqi_test_pub_account_access_token'):
        return redis_conn.get('zhangjiaqi_test_pub_account_access_token')

    result = requests.get(url=wx_secrets.ACCESS_TOKEN_URL,
                          params={
                              'grant_type': 'client_credential',
                              'appid': wx_secrets.WX_APPID,
                              'secret': wx_secrets.WX_APPSECRET
                          }).json()
    access_token = result.get('access_token', None)

    redis_conn.set('zhangjiaqi_test_pub_account_access_token', access_token, ex=7200)

    print('===》', access_token)

    return access_token


if __name__ == '__main__':
    pass
