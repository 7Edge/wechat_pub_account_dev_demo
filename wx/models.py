import hashlib

from django.db import models


# Create your models here.

# 用户表
class Users(models.Model):
    loginname = models.CharField(verbose_name='登陆用户名', max_length=64, unique=True)
    password = models.CharField(verbose_name='登陆密码', max_length=255)
    uid = models.CharField(verbose_name='唯一ID', max_length=255, help_text='用户名的md5值,不用填写', blank=True)
    nickname = models.CharField(verbose_name='昵称', max_length=64)

    wx_openid = models.CharField(verbose_name='OpenID', max_length=255, blank=True)

    class Meta:
        verbose_name_plural = '001. 用户表'

    def save(self, *args, **kwargs):
        # uid的值是loginname字段的MD5值，所以在写到数据库save前，要将uid设置，所以重写save
        # 通过判定，pk是否存在来断定是新建数据，而不是已存在的数据。

        if not self.pk or not self.uid:
            md5_obj = hashlib.md5()
            md5_obj.update(self.loginname.encode('utf-8'))
            self.uid = md5_obj.hexdigest()
        super(Users, self).save(*args, **kwargs)
