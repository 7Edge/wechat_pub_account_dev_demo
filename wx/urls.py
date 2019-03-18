#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: urls
# Date: 3/18/2019

from django.urls import re_path

from .views import wx_check

urlpatterns = [
    re_path('wx_check/$', wx_check),
]

if __name__ == '__main__':
    pass
