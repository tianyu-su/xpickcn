import re
import threading
from urllib.parse import urlsplit

import requests
from django.contrib.auth.models import Group
from django.http import JsonResponse

from backend.api.models import *
from backend.settings.dev import USER_DEFAULT_PWD, DOMAIN_PRESERVE


def get_second_domain(host):
    host = host.rsplit('.', 3)
    if len(host) > 2:
        return host[-3]
    else:
        return 'www'


def init_new_web_user(web_domain, obj=None):
    # 创建用户
    if obj is None:
        web_user = WebUser()
        web_user.u_website_domain = web_domain
        web_user.set_password(USER_DEFAULT_PWD)
        web_user.save()
    else:
        web_user = obj
    # 添加默认组
    group = Group.objects.get(name='普通用户')
    group.user_set.add(web_user)
    # group.save()
    # web_user.groups.add(group)
    # web_user.save()
    # 初始化 www 内容和当前用户
    www_user = WebUser.objects.get(u_website_domain='www')
    cates = Category.objects.filter(user=www_user)
    for cate in cates:
        ncate = Category.objects.create(cate_name=cate.cate_name, cate_class=cate.cate_class,
                                        user=web_user)
        books = BookMark.objects.filter(cate=cate)
        for book in books:
            BookMark.objects.create(url=book.url, img=book.img, title=book.title, desc=book.desc,
                                    cate=ncate, user=web_user)

    return web_user


def web_domain_check(web_domain, superadmin=False):
    ret = False
    msg = ''
    if re.match("^[a-z][a-z0-9]{2,20}$", web_domain) is None:
        msg = '用户名非法，只允许输入以字母开头的小写字母和数字，长度不超过20！'
    elif web_domain in DOMAIN_PRESERVE:
        msg = f'该名字 {web_domain} 禁止注册！请更换！'
    else:
        ret = True
    if superadmin:
        ret = True
    return ret, msg


def cors_proble(dic):
    """
    解决跨域请求问题
    dic: dict 后台要返回数据
    """
    response = JsonResponse(dic, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def get_website_domain(bookmark: BookMark):
    fetch = get_website_favicon_url(bookmark.url)
    bookmark.img = fetch
    bookmark.save()


def get_website_favicon_url(url):
    deault = 'https://i.loli.net/2020/08/06/ZSnQ3b8GCoOWVmh.png'
    hostname = urlsplit(url).hostname
    www_url = '.'.join(['www'] + hostname.rsplit('.', 2)[-2:])
    pub_api = 'http://favicongrabber.com/api/grab/{}'
    max_size, max_icon_url = -1, None
    response = requests.get(pub_api.format(www_url)).json()
    if response.get('error'):
        return deault
    for icon in response.get('icons'):
        if icon['src'].rfind('svg') != -1:
            return icon['src']
        if icon.get('sizes', None):
            sx = icon['sizes'].find('x')
            if sx != -1:
                size = int(icon['sizes'][:sx])
                if size > max_size:
                    max_size = size
                    max_icon_url = icon['src']
    print('done')
    if max_size != -1:
        return max_icon_url
    else:
        fi = response.get('icons')[0]['src']
        if fi.find('data:image/x-icon') != -1:
            return deault
        else:
            return fi


# threading.Thread(target=get_website_favicon_url, args=('https://i.loli.net/2020/08/06/ZSnQ3b8GCoOWVmh.png',)).start()
