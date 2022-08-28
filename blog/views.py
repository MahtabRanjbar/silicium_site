from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Article, Category


# Create your views here.
def home(request):
    articles = Article.objects.filter(status='p')
    categories = Category.objects.filter(status=True)   
    context = {'articles': articles,
               'categories': categories}
    return render(request, 'blog/index.html', context)


def detail_view(request, slug):
    query = get_object_or_404(Article, slug=slug)
    context = {'article': query}
    return render(request, 'blog/detail.html', context=context)
    

def category_view(request, slug):
    context = {'categories': get_object_or_404(Category, slug=slug)}
    return render(request, 'blog/category.html', context)
    