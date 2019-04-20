#coding:utf-8
"""SongCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog.feed import AllAriclesRssFeed
import xadmin

'''Django匹配URL是在该项目目录下的urls.py中完成，因此，要把blog应用下的urls.py包含到该文件中，
'''
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^blog/',include('blog.urls')), #Django将r后面的字符串和后面的include的urls.py文件进行拼接
    url(r'',include('comments.urls')),
    url(r'^all/rss/$',AllAriclesRssFeed(),name='rss'), #设置首页面RSS的URL为/all/rss
    url(r'^search/',include('haystack.urls')), #这里的urls.py Django已经帮我们写好了,只要有在settings.py中配置
]
