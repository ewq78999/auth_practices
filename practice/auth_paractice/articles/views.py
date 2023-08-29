from django.shortcuts import render, redirect
from . models import Article
from . forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    
    articles = Article.objects.all()
    form = CommentForm()

    context = {
        'articles' : articles,
        'form' : form,
    }

    return render(request, 'index.html', context)

@login_required
def create(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')

    else:
        form = ArticleForm()

    context = {
        'form' : form,
    }

    return render(request, 'form.html', context)

@login_required
def comment_create(request, article_id):
    article = Article.objects.get(id=article_id)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()

        return redirect('article:index')

