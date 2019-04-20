#coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('blog.Article')

    class Meta:
        verbose_name_plural = verbose_name = u'评论'

    def __unicode__(self):
        return self.text[:20]
