from django import forms
from .models import ArticlePost
from mdeditor.fields import MDTextFormField

class ArticlePostForm(forms.ModelForm):
        class Meta:

                model=ArticlePost
                #表单包含的字段
                fields=('title','body')


