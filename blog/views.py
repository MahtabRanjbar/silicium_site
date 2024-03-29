from datetime import datetime, timedelta

from accounts.mixins import AuthorAccessMixin
from accounts.models import CustomUser
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from blog.models import Article, Category


# Create your views here.
# based on FBV
class ArticleList(ListView):
    last_month = datetime.today() - timedelta(days=30)
    queryset = Article.objects.published().annotate(
        count=Count("hits", filter=Q(articlehit__created_at__gt=last_month))
        ).order_by('-count', '-published_at')
    queryset = Article.objects.published()
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 2


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address 
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    
 


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    

class CategoryList(ListView):
    paginate_by = 2
    template_name = 'blog/category.html'
    context_object_name = 'articles'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.published(), slug=slug)
        return category.article.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 2
    template_name = 'blog/author_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(CustomUser, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
