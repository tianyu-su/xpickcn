""" Production Settings """

# import dj_database_url
from .dev import *

############
#   CDN    #
############

# CDN 加速admin引用过的文件,其实就是把 {% static "admin/css/login.css" %} 这里面的 static 给换掉了
# tmp::STATIC_URL = 'https://cdn.jsdelivr.net/gh/tianyu-su/xpickcn@1.0/dist/static/'
###@@########CND URL PLACEHOLDER ####@@####

############
# DATABASE #
############
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.getenv('DATABASE_URL')
#     )
# }


############
# SECURITY #
############

DEBUG = bool(os.getenv('DJANGO_DEBUG', ''))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['xpick.cn']
