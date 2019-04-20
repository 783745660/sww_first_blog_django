#coding=utf-8

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import  AbstractUser,User
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')  # 昵称
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=20, choices=(('male', u'男'), ('female', '女')), default='female')
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')
    phonenumber = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        '''定义表的Meta信息
        '''
        #定义在管理后台显示的名称
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username  # 因为我们已经继承了AbstractUser,而这里的username在AbstractUser这个类中


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,unique=True,verbose_name=u'类别')
    desc = models.TextField(verbose_name=u'详情')

    class Meta:
        verbose_name_plural = verbose_name = u'类别'

    def __unicode__(self):
            return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'标签')

    class Meta:
        verbose_name_plural = verbose_name = u'标签'

    def __unicode__(self):
        return self.name

# class Comment(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField('评论用户', max_length=20)
#     email = models.EmailField('邮箱')
#     content = models.TextField('内容')
#     publish = models.DateField('时间', auto_now=True)
#     article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='文章')
#     reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='回复')
#
#     class Meta:
#         verbose_name_plural = verbose_name = '评论'
#
#     def __str__(self):
#         return self.content


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,verbose_name=u'作者')
    title =  models.CharField(max_length=50,verbose_name=u'标题')
    abstract = models.CharField(max_length=300,blank=True,verbose_name=u'摘要')
    content = models.TextField(verbose_name=u'内容',default='')
    category = models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=1,verbose_name=u'类别')
    pub_date = models.DateField(auto_now_add=True,editable=True)
    tag = models.ManyToManyField(Tag,verbose_name=u'标签')
    picture = models.CharField(max_length=200,blank=True)   #标题图片地址
    views_num = models.PositiveIntegerField(default=0)  # PositiveIntegerField 类型只允许值为非负整数

    class Meta:
        verbose_name_plural = verbose_name = u'文章'
        ordering = ['-pub_date'] #Django允许我们直接在model.Model的子类中定义一个Meta类，在这个类中指定一些属性来规定子类属性

    def __unicode__(self):
        return self.title


    ''' 01增加Article模型方法 
        在article类中定义一个get_absolute_url方法，生成自己的url
        这里的reverse函数第一个参数值是'blog:detail'，意思是blog应用下的name=detail函数（blog/urls.py中定义）
        第二个参数是将detail的正则表达式参数被后面的参数pk换掉，最终生成一个article/24这样的URL
    '''
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})


    '''02增加Aticle模型方法
        一旦用户访问了某篇文章，这时将views_num值 +1， 由于这个过程较为单一，因此最好在模型子类中自定义。
    '''
    def increase_views_num(self):
        self.views_num += 1    #将自身值+1
        self.save(update_fields=['views_num'])#然后将调用save方法将其保存在数据库中，Django 中使用update_field字段来更新数据库中的views_num字段


    '''03 复写save方法从文章内容中提取前N个字符作为文章的摘要
        但前提是在admin后台并未为文章添加摘要
    '''
    def save(self,*args,**kwargs):
        if not self.abstract:
            '''这里要用markdown的目的是可能我们在后台添加的文章有一定的格式如富文本形式，
                我们需要先转为HTML文本形式，然后再去掉HTML标签
            '''
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra', # 先转为HTML文本，
                'markdown.extensions.codehilite',  # 然后去掉HTML文本中的标签
            ])

            self.abstract = strip_tags(md.convert(self.content))[:54]

        #调用父类的save方法，将数据保存在数据库中
        super(Article,self).save(*args,**kwargs)

