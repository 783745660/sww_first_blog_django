#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/15 16:51'

import xadmin

'''定制Admin后台数据显示
'''
from .models import Article,Category,Tag

class ArticleAdmin(object):
    list_display = ('title','content','category','author','pub_date','tag','abstract')

class CategoryAdmin(object):
    list_display = ('name','desc')

class TagAdmin(object):
    list_display = ('name','id')

class CommentAdmin(object):
    list_display = ('name','content','article','publish')


'''注册数据模型
'''
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Tag,TagAdmin)
