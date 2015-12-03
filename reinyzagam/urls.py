#coding=utf8
"""reinyzagam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url

# REST - Przeglądanie API
from rest_framework.urlpatterns import format_suffix_patterns

from User import views, serializers

urlpatterns = format_suffix_patterns([
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^rest/$', views.api_root),

    # REST
    url(r'^rest/users_list/$', views.users_list, name='users_list'),
    url(r'^rest/user_detail/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail')
])
