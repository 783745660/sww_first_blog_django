#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/16 22:08'

from django.conf.urls import url
from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/artcile/(?P<article_pk>[0-9]+)/$',views.article_commnet,name='article_comment'),
]