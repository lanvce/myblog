import markdown
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
# 视图函数
def article_list(request):
    articles=ArticlePost.objects.all()

    context={'articles':articles}

    return render (request,'article/list.html',context)

def article_detail(request,id):
    article=ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])

    context={'article':article}
    return render(request,'article/detail.html',context)


def article_create(request):
    #如果为post请求
    if request.method=='POST':
        #将post的data给表单实例
        article_post_form=ArticlePostForm(data=request.POST)
        #看是否符合模型要求
        if article_post_form.is_valid():
            #保存数据 但不提交
            new_article=article_post_form.save(commit=False)
            #作者为数据库中id=1的用户为作者
            new_article.author=User.objects.get(id=1)
            #保存提交到数据库中
            new_article.save()
            #写完后返回到文章列表
            return redirect("article:article_list")
        else:
            return HttpResponse("表单填写错误，请重新填写")

    else:
        article_post_form=ArticlePostForm ()
        context={'article_post_form':article_post_form}
        return render(request,'article/create.html',context)
# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

#修改文章
def article_update(request,id):

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)

