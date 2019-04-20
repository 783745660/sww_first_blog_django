#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/15 20:32'

from django.conf.urls import url
from . import views

'''这里将url与视图函数绑定:
    这里的(?P<pk>[0-9]+)是由python定义匹配规则，
    作用是从用户访问的URL里把括号内匹配的字符串捕获出来，并传递对应的视图函数detail。
    实际上视图函数调用方式如detail(request,pk=255)
'''

'''app_name='blog' 告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间 
'''
app_name = 'blog'


#URL与视图函数的绑定,url()中的第二个参数必须是函数，
# 而IndexView是一个类，因此使用类视图的as_view()方法将其转换为视图函数
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^arcticle/(?P<pk>[0-9]+)/$',views.ArticleDetailView.as_view(),name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
]