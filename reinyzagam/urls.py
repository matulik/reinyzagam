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

from User import views as user_views
from Store import views as store_views


urlpatterns = format_suffix_patterns([
    url(r'^$', user_views.login),
    url(r'^login/$', user_views.login),
    url(r'^logout/$', user_views.logout),
    url(r'^rest/$', user_views.api_root),

    ### REST
    ## User
    url(r'^rest/users_list/$', user_views.users_list, name='users_list'),
    url(r'^rest/user_detail/(?P<pk>[0-9]+)/$', user_views.user_detail, name='user_detail'),

    ## Store
    # Location
    url(r'^rest/locations_list/$', store_views.locations_list, name='locations_list'),
    url(r'^rest/location_detail/(?P<pk>[0-9]+)/$', store_views.location_detail, name='location_detail'),

    # Buyer
    url(r'^rest/buyers_list/$', store_views.buyers_list, name='buyers_list'),
    url(r'^rest/buyer_detail/(?P<pk>[0-9]+)/$', store_views.buyer_detail, name='buyer_detail'),

])
