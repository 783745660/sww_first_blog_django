#coding=utf-8
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Article

from .models import Comment
from .forms import CommentForm

# Create your views here.
'''comments/views.py中article_comments()函数的作用是处理用户提交的评论表单
'''
def article_commnet(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article  #将被评论的文章和评论关联起来
            comment.save()
            return redirect(article)
        else:
            comment_list = article.comment_set.all()
            context = {'article':article,
                       'form':form,
                       'comment_list':comment_list
                       }
            return render(request,'blog/detail.html',context=context)

    #如果不是post请求，说明用户没有提交数据，即重定向到文章的详情页
    else:
        return redirect(article)