from django.shortcuts import render, get_object_or_404, get_list_or_404

from blog.models import Article


# Create your views here.
def home(request):
    query = Article.objects.filter(status='p').order_by('-published_at')
    context = {'articles': query}
    return render(request, 'blog/index.html', context)


def detail_view(request, slug):
    query = get_object_or_404(Article, slug=slug, status='p')
    context = {'article': query}
    return render(request, 'blog/detail.html', context=context)
    
