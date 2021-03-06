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
from webapp import views


urlpatterns = format_suffix_patterns([
    # webapp urls
    url(r'^choose/$', views.choose),
    url(r'^webapp/locations/$', views.locations),

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

    # Buyer
    url(r'^rest/categories_list/$', store_views.categories_list, name='categories_list'),
    url(r'^rest/category_detail/(?P<pk>[0-9]+)/$', store_views.category_detail, name='category_detail'),

    # Article
    url(r'^rest/articles_list/$', store_views.articles_list, name='articles_list'),
    url(r'^rest/article_detail/(?P<pk>[0-9]+)/$', store_views.article_detail, name='article_detail'),

    # Order
    url(r'^rest/orders_list/$', store_views.orders_list, name='orders_list'),
    url(r'^rest/order_detail/(?P<pk>[0-9]+)/$', store_views.order_detail, name='order_detail'),

    # ArticleUnit
    url(r'^rest/articleunits_list/$', store_views.articleunits_list, name='articleunits_list'),
    url(r'^rest/articleunit_detail/(?P<pk>[0-9]+)/$', store_views.articleunit_detail, name='articleunit_detail'),

])
