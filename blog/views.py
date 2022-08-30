from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DeleteView, ListView

from blog.models import Article, Category


# Create your views here.
# based on FBV
class ArticleList(ListView):
    queryset = Article.objects.published()
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 2


class ArticleDetail(DeleteView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)
    template_name = 'blog/detail.html'
    context_object_name = 'article'


def category_view(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug)
    articles_list = category.article.published()
    paginator = Paginator(articles_list, 2)
    articles = paginator.get_page(page)
    context = {'category': category,
               'articles': articles}
    return render(request, 'blog/category.html', context)
