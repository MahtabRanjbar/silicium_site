from django.shortcuts import render, get_object_or_404, get_list_or_404

from blog.models import Article, Category


# Create your views here.
def home(request):
    articles = Article.objects.filter(status='p')
    categories = Category.objects.filter(status=True)   
    context = {'articles': articles,
               'categories': categories}
    return render(request, 'blog/index.html', context)


def detail_view(request, slug):
    query = get_object_or_404(Article, slug=slug, status='p')
    context = {'article': query}
    return render(request, 'blog/detail.html', context=context)
    
