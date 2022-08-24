from django.shortcuts import render

from blog.models import Article


# Create your views here.
def home(request):
    query = Article.objects.filter(status='p').order_by('-published_at')
    context = {'articles': query}
    return render(request, 'blog/index.html', context)


def detail_view(request, slug):
    query = Article.objects.get(slug=slug)
    context = {'article': query}
    return render(request, 'blog/post.html', context=context)
    
