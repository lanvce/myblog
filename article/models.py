import django
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ArticlePost(models.Model):
    #on_delete 指定删除方式
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    title=models.CharField(max_length=100)

    body=MDTextField()

    created=models.DateTimeField(default=timezone.now)

    updated=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=('-created',)

    def __str__(self):
        return self.title

