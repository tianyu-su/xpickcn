import six
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


# class Message(models.Model):
#     subject = models.CharField(max_length=200)
#     body = models.TextField()
#
#
# class MessageSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Message
#         fields = ('url', 'subject', 'body', 'pk')


class WebUserManager(BaseUserManager):
    """
    配合自定义User使用
    """

    def create_superuser(self, u_website_domain, email, password):
        if not u_website_domain:
            raise ValueError('The web_site_domain must be set')
        email = self.normalize_email(email)
        u_website_domain = self.model.normalize_username(u_website_domain)
        user = self.model(u_website_domain=u_website_domain, email=email)
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class WebUser(AbstractBaseUser, PermissionsMixin):
    """
    继承抽象基本用户为了使用其用户认证，permissionsMixin 使用权限系统
    """
    # validators=[validators.RegexValidator("^[a-z][a-z0-9]{2,20}$", message='用户名非法，只允许输入以字母开头的小写字母和数字，长度不超过20！')]

    u_website_domain = models.CharField('二级域名', max_length=20, unique=True, help_text='用于获取自己的导航网址',
                                        error_messages={'unique': '该名字已被注册！请更换！'})
    u_last_visit_time = models.DateTimeField('最后访问时间', default=timezone.now)
    u_top_frequency = models.SmallIntegerField('常用推荐数量', default=10)

    email = models.EmailField('Email', blank=True)

    def total_use_item(self):
        total = 0
        items = BookMark.objects.filter(user=self)
        for item in items:
            total += item.bm_click_times
        return format_html('<span class="text">{}</span>', total)

    total_use_item.short_description = format_html(
        '<span class="text">使用次数</span>')

    def __str__(self):
        return self.u_website_domain

    # 必须写，在 Manager 中有使用
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'u_website_domain'

    # 自定义必须实现 Manager
    objects = WebUserManager()

    def get_short_name(self):
        return self.u_website_domain

    def get_full_name(self):
        return self.get_short_name()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True

    def has_group(self, group):
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        if not hasattr(self, '_group_cache'):
            self._group_cache = set([g.name for g in self.groups.all()])
        return group in self._group_cache

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-u_last_visit_time']


class OAuthQQModel(models.Model):
    u_openid = models.CharField('QQ_openid', max_length=64, primary_key=True)
    u_nick_name = models.CharField('QQ_nickname', max_length=64)
    u_gender = models.CharField('QQ_gender', max_length=4)
    u_img = models.URLField('QQ_image')

    def thumb_show(self):
        return format_html(
            '<span style="text-align: center;display:block;" ><a href="{}"><img src="{}" width="20px" height="20px"/></a></span>',
            self.u_img, self.u_img)

    thumb_show.short_description = format_html(
        '<span style="text-align: center;display:block;"  class="text">缩略图</span>')

    user = models.ForeignKey(WebUser, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='用户')

    def __str__(self):
        return self.u_nick_name

    class Meta:
        verbose_name = 'QQ授权信息'
        verbose_name_plural = 'QQ授权信息'


class CategoryIcon(models.Model):
    ci_class = models.CharField('分类图标', max_length=32)

    def __str__(self):
        # return self.ci_class[len("linecons-"):]
        return self.ci_class

    def thumb_show(self):
        return format_html(
            '<span ><i class="{}"></i></span>', self.ci_class)

    thumb_show.short_description = format_html('<span  class="text">缩略图</span>')

    class Meta:
        verbose_name = '导航栏类别图标'
        verbose_name_plural = '导航栏类别图标'


class Category(models.Model):
    user = models.ForeignKey(WebUser, on_delete=models.CASCADE, verbose_name='用户')
    cate_class = models.ForeignKey(CategoryIcon, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='书签类别图标')
    cate_name = models.CharField('分类名称', max_length=64)

    def __str__(self):
        return self.cate_name

    class Meta:
        verbose_name = '书签类别'
        verbose_name_plural = '书签类别'


class BookMark(models.Model):
    url = models.URLField('网址')
    img = models.URLField('ICON', default='https://i.loli.net/2020/08/06/ZSnQ3b8GCoOWVmh.png')
    title = models.CharField('书签名字', max_length=64)
    desc = models.CharField('备注', max_length=125, blank=True, default='')
    bm_click_times = models.IntegerField('点击次数', default=0)

    cate = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='书签类别')
    user = models.ForeignKey(WebUser, on_delete=models.CASCADE, default=1, verbose_name='用户')

    def thumb_show(self):
        return format_html(
            # '<span > <a href="{}"><img src="{}" width="20px" height="20px"/></a></span>',
            '<span > <img src="{}" width="20px" height="20px"/></span>',
            self.img, self.img)

    thumb_show.short_description = format_html(
        '<span class="text" >网站图标</span>')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '书签'
        verbose_name_plural = '书签'
