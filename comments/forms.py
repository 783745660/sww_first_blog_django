#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/4/16 21:36'

from django import forms
from .models import Comment

'''表单用来收集并向服务器提交用户输入的数据，当用户想要发表评论时，
    根据表单要求发表评论，之后点击评论按钮，这些数据就会发送给某个URL，
    每一个URL对应一个视图函数来处理用户通过表单提交的数据，
    如果合法，那么Django就会将其写入到数据库中，如果不合法，Django就会将错误信息返回给用户，要求用户重新输入合法数据格式
'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        '''model = Comment 表明这个表单对应的数据库模型是 Comment 类
            fields指明表单要显示的字段
        '''
        fields = ['name','email','url','text']
