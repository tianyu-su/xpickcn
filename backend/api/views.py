import collections
import json
import re
import time

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect, HttpResponse, render
from django.views.generic import TemplateView

from .models import *
from .oauth_client import OAuthQQ
from .utils import get_second_domain, init_new_web_user, web_domain_check
from ..settings.dev import USER_DEFAULT_PWD

index_view = TemplateView.as_view(template_name='index.html')


##############################################################
######                       qq bind                      ####
##############################################################
# QQ login :https://www.jianshu.com/p/76f9682634e2
def qq_login(request):
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)


def qq_check(request):  # 第三方QQ登录，回调函数
    """登录之后，会跳转到这里。需要判断code和state"""
    if request.use.is_authenticated:
        return HttpResponseRedirect(f'/api/admin/')
    request_code = request.GET.get('code')
    oauth_qq = OAuthQQ(settings.QQ_APP_ID, settings.QQ_KEY, settings.QQ_RECALL_URL)

    # 获取access_token
    access_token = oauth_qq.get_access_token(request_code)
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    open_id = oauth_qq.get_open_id()
    print(open_id)
    # return HttpResponse('<h1>欢迎你,{}.</h1>'.format(open_id))

    # 检查open_id是否存在
    qq_open_id = OAuthQQModel.objects.filter(u_openid=str(open_id))
    print(qq_open_id)

    # 不管是否存在全部返回主页面
    # 不存在：index?open
    infos = oauth_qq.get_qq_info()  # 获取用户信息
    url = '%s?open_id=%s&nickname=%s' % ('/static/bindpage.html', open_id, infos['nickname'])
    if len(qq_open_id):
        # 存在则获取对应的用户，并登录
        user = qq_open_id[0].user
        if user:
            return inner_jump_auth(request, user.u_website_domain)
        else:
            return HttpResponseRedirect(url)
    else:
        # 不存在，则跳转到绑定用户页面
        OAuthQQModel.objects.create(u_openid=open_id, u_nick_name=infos['nickname'], u_gender=infos['gender'],
                                    u_img=infos['figureurl_qq_1'])
        return HttpResponseRedirect(url)


def bind_account(request):
    if request.method == 'POST':
        open_id = request.POST.get('open_id', '')
        web_domain = request.POST.get('web_domain', '')
        return create_web_user(request, open_id, web_domain)
    # else:
    #     testing...
    #     url = '%s?open_id=%s&nickname=%s' % ('/static/bindpage.html', 'open_id', '昵称')
    #     return HttpResponseRedirect(url)


def inner_jump_auth(request, website_domain):
    user = authenticate(u_website_domain=website_domain, password=USER_DEFAULT_PWD)
    login(request, user)
    return HttpResponseRedirect(f'{request.scheme}://{website_domain}.xpick.cn:{request.get_port()}/api/admin/')


def create_web_user(request, open_id, web_domain):
    ret = {'code': -1, 'msg': ''}

    qq_entity = OAuthQQModel.objects.filter(u_openid=open_id)
    if len(qq_entity) == 0:
        return HttpResponse(status=403)
    else:
        valid, msg = web_domain_check(web_domain)
        if not valid:
            ret['msg'] = msg
            return HttpResponse(json.dumps(ret), content_type="application/json")
        try:
            if qq_entity[0].user:
                ret['msg'] = f"你已经拥有自己的导航域名：{request.scheme}://{qq_entity[0].user.u_website_domain}.xpick.cn，不可以重复注册！"
            else:
                # 绑定 QQ_OA
                qq_entity[0].user = init_new_web_user(web_domain)
                qq_entity[0].save()

                ret['code'] = 0
                ret['msg'] = f'{web_domain}.xpick.cn'
        except Exception as e:
            # print(e)
            ret['msg'] = '域名重复，请重新填写。'
        finally:
            return HttpResponse(json.dumps(ret), content_type="application/json")


##############################################################
######                   expose interface                 ####
##############################################################
def add_one(request, bookmark_id):
    mark = BookMark.objects.filter(pk=bookmark_id)
    if mark:
        aitem = mark[0]
        aitem.bm_click_times += 1
        aitem.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def get_user_preference(request):
    second_domain = get_second_domain(request.headers.get('host'))
    user = WebUser.objects.get(u_website_domain=second_domain)
    user.u_last_visit_time = timezone.now()
    user.save()

    # json
    cates = Category.objects.filter(user=user)
    ret = collections.OrderedDict()
    ret['常用推荐'] = {'icon': 'linecons-star',
                   'data': list(BookMark.objects.filter(user=user).order_by('-bm_click_times').values
                                ('id', 'img', 'url', 'title', 'desc')[:user.u_top_frequency])}
    for cate in cates:
        items = BookMark.objects.filter(cate=cate).values('id', 'img', 'url', 'title', 'desc')
        if len(items):
            ret[cate.cate_name] = {'data': list(items), 'icon': cate.cate_class.ci_class}

    return HttpResponse(json.dumps(ret), content_type="application/json")
