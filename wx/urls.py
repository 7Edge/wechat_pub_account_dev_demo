#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: urls
# Date: 3/18/2019

from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^wx_check/$', views.wx_check),
    re_path('^bind_wx/$', views.bind_wx, name='bind_wx'),
    re_path('^login/$', views.login, name='login'),
    re_path('^callback_bind_wx/$', views.to_bind_wx, name='callback_bind_wx'),
    re_path('^get_authorize_url/$', views.get_authorized_url, name='get_authorized_url'),
]

if __name__ == '__main__':
    pass
