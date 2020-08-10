# 如何启动新网站

## 配置 Setting
1. 修改 QQ 认证的相关参数

## 清空数据库
删除 db.sqlit3
删除 backend/api/migarations 文件夹

## 重建数据库
1. python manage.py makemigrations api
2. python manage.py migrate

## 导入初始数据(分类图标，初始权限组)
1. python manage.py loaddata init_website.json
> python manage.py dumpdata api.categoryicon auth > init_website.json
> 产生 初始的权限表和目录图标

## 创建超级用户 www
www也是公共导航
1. python manage.py createsuperuser

## 复制本机的 dev.py 到服务器的setting文件夹
## 运行 update_web.sh
