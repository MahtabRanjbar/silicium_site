from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator
from blog.models import Article, Category


# Create your views here.
def home(request, page=1):
    article_list = Article.objects.published()
    categories = Category.objects.filter(status=True)

    paginator = Paginator(article_list, 2)
    articles = paginator.get_page(page)
    context = {'articles': articles,
               'categories': categories}
    return render(request, 'blog/index.html', context)


def detail_view(request, slug):
    query = get_object_or_404(Article, slug=slug)
    context = {'article': query}
    return render(request, 'blog/detail.html', context=context)


def category_view(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug)
    articles_list = category.article.published()
    paginator = Paginator(articles_list, 2)
    articles = paginator.get_page(page)
    context = {'category': category,
               'articles': articles}
    return render(request, 'blog/category.html', context)
