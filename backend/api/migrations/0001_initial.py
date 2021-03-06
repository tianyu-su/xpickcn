# Generated by Django 2.2 on 2020-08-08 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('u_website_domain', models.CharField(error_messages={'unique': '该名字已被注册！请更换！'}, help_text='用于获取自己的导航网址', max_length=20, unique=True, verbose_name='二级域名')),
                ('u_last_visit_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后访问时间')),
                ('u_top_frequency', models.SmallIntegerField(default=10, verbose_name='常用推荐数量')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-u_last_visit_time'],
            },
        ),
        migrations.CreateModel(
            name='CategoryIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci_class', models.CharField(max_length=32, verbose_name='分类图标')),
            ],
            options={
                'verbose_name': '导航栏类别图标',
                'verbose_name_plural': '导航栏类别图标',
            },
        ),
        migrations.CreateModel(
            name='OAuthQQModel',
            fields=[
                ('u_openid', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='QQ_openid')),
                ('u_nick_name', models.CharField(max_length=64, verbose_name='QQ_nickname')),
                ('u_gender', models.CharField(max_length=4, verbose_name='QQ_gender')),
                ('u_img', models.URLField(verbose_name='QQ_image')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': 'QQ授权信息',
                'verbose_name_plural': 'QQ授权信息',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_name', models.CharField(max_length=64, verbose_name='分类名称')),
                ('cate_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.CategoryIcon', verbose_name='书签类别图标')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '书签类别',
                'verbose_name_plural': '书签类别',
            },
        ),
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='网址')),
                ('img', models.URLField(default='https://i.loli.net/2020/08/06/ZSnQ3b8GCoOWVmh.png', verbose_name='ICON')),
                ('title', models.CharField(max_length=64, verbose_name='书签名字')),
                ('desc', models.CharField(blank=True, default='', max_length=125, verbose_name='备注')),
                ('bm_click_times', models.IntegerField(default=0, verbose_name='点击次数')),
                ('cate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category', verbose_name='书签类别')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '书签',
                'verbose_name_plural': '书签',
            },
        ),
    ]
