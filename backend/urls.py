"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path

from .api.views import index_view, add_one, get_user_preference, bind_account, qq_login, qq_check

# router = routers.DefaultRouter()
# router.register('messages', MessageViewSet)

urlpatterns = [

    path('', index_view),
    path('bindpage/', bind_account),

    path('api/<int:bookmark_id>/', add_one),
    path('api/mine/', get_user_preference),

    path('api/admin/', admin.site.urls),

    # QQ OAuth
    path('oauth/qq/login/', qq_login),
    path('oauth/qq/check/', qq_check),

]
