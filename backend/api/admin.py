import re
import threading
import urllib.parse as parse

from django.contrib import messages

import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext as _, ngettext

from .models import *

# Register your models here.
from .utils import init_new_web_user, get_website_domain

admin.site.site_header = "口袋导航"
admin.site.site_title = "口袋导航"


# 重写UserAdmin类
@admin.register(WebUser)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新增，设置默认密码, 修改密码只能通过页面右上角修改密码进行
            from backend.settings.dev import USER_DEFAULT_PWD
            obj.set_password(USER_DEFAULT_PWD)
            obj.save()
            init_new_web_user(obj.u_website_domain, obj)
        else:
            obj.save()

    # 实现外键表链接到本页面一起编辑
    list_display = ('u_website_domain', 'total_use_item', 'u_top_frequency', 'last_login', 'u_last_visit_time')
    list_editable = ['u_top_frequency']
    readonly_fields = ['last_login', 'u_last_visit_time']
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ('基本信息', {'fields': ['u_website_domain', 'u_top_frequency', 'last_login',
                                     'u_last_visit_time', 'is_superuser', 'groups', 'user_permissions']}),
            )
        else:
            return (
                ('基本信息', {'fields': ['u_website_domain', 'u_top_frequency']}),
            )

    # 非超级管理员只显示自己信息
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(pk=request.user.id)


@admin.register(OAuthQQModel)
class OAuthQQModelAdmin(admin.ModelAdmin):
    list_display = ['u_openid', 'u_nick_name', 'u_gender', 'thumb_show']


@admin.register(CategoryIcon)
class CategoryIconAdmin(admin.ModelAdmin):
    list_display = ['ci_class', 'thumb_show', 'ci_name']
    ordering = ('ci_name',)
    list_editable = ['ci_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['cate_name', 'cate_img', 'user']
        return ['cate_name', 'cate_img']

    # 非超级管理员只显示自己信息
    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ('基本信息', {'fields': ['cate_class', 'cate_name', 'user']}),
            )
        else:
            return (
                ('基本信息', {'fields': ['cate_class', 'cate_name']}),
            )

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()


@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['title', 'thumb_show', 'url', 'desc', 'bm_click_times', 'cate', 'user']
        return ['title', 'thumb_show', 'url', 'desc', 'bm_click_times', 'cate', ]

    search_fields = ['url', 'title', 'desc']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['user', 'cate']
        else:
            return ['cate']

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()
        threading.Thread(target=get_website_domain, args=(obj,)).start()

    # 非超级管理员只显示自己信息
    def get_queryset(self, request):
        qs = super(BookMarkAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                ('基本信息', {'fields': ['url', 'title', 'desc', 'bm_click_times', 'cate', 'user']}),
            )
        else:
            return (
                ('基本信息', {'fields': ['cate', 'url', 'title', 'desc', 'bm_click_times']}),
            )

    readonly_fields = ['bm_click_times']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "cate":
                kwargs["queryset"] = Category.objects.filter(user=request.user)
        return super(BookMarkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
