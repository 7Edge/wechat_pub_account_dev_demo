from django.test import TestCase

# Create your tests here.

import django.contrib.sessions.middleware

import django.contrib.sessions.backends.db

from django.contrib.auth import login

from datetime import datetime

from django.db import models

import django_redis


import redis

from django.core.cache.backends.base import BaseCache
from django_redis.cache import omit_exception