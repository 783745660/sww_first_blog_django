#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/16 16:46'

'''为避免在每一个视图函数中书写大量从数据库中获取数据的代码，这里用模板标签来实现数据获取
    即定义标签函数，用标签函数获取数据，然后在模板中调用这些标签函数即可，
    最终通过模板将数据渲染出来；
'''
from django import template
from django.db.models.aggregates import Count
from ..models import Article,Category,Tag


'''将该标签函数注册在模板中，一般让模板知道如何使用它
    这样就可以在模板中使用语法 {% get_recent_articles %} 调用这个函数了。
'''
register = template.Library()


'''01获取最近文章
'''
@register.simple_tag
def get_recent_artciles(num=5):
    return Article.objects.all().order_by('-pub_date')[:num]


'''02归档模板标签： 获取文章创建时间的列表
'''
@register.simple_tag
def archives():
    return Article.objects.dates('pub_date','month',order='DESC')  #以文章发表月份划分


'''03获取文章分类
'''
@register.simple_tag
def get_categories():
    #这里的Category.objects.annotate方法也会返回数据库中全部的Category记录，
    # 但是使用Cout()方法返回与每条category记录关联的Article记录的行数
    #使用filter()过滤器过滤掉文章数小于1的分类，即如果该分类下没有文章，那么就不显示该分类
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)


'''04 获取标签列表
'''
@register.simple_tag
def get_tags():
    #这里的Tag.objects.annotate方法也会返回数据库中全部的Tag记录，
    # 但是使用Count()方法返回与每条tag记录关联的Article记录的行数
    #使用filter()过滤器过滤掉文章数小于1的标签，即如果该标签下没有文章，那么就不显示该标签
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

