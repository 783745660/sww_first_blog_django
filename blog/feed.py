#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/18 22:03'

from django.contrib.syndication.views import Feed
from .models import Article


'''该代码块的作用是实现一个聚合阅读订阅器,并用chrome中的RSS Feed Reader应用实现
'''
class AllAriclesRssFeed(Feed):
    title = 'Django个人博客项目'  #订阅器的标题
    link = '/'     #                #
    description = 'Django个人博客项目测试'

    def items(self):  #显示所有的文章内容条目
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' %(item.category,item.title)  #显示文章内容条目的分类和标题

    def item_description(self, item):
        return item.content   #通过上文定义的items()方法获取article的内容