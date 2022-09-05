from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import FieldsMixin, AuthorAccessMixin, SuperUserAccessMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/adminlte/home.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all() 
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FieldsMixin, CreateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status']
    template_name = 'registration/adminlte/article-create-update.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all() 
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, UpdateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status' ]
    template_name = 'registration/adminlte/article-create-update.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all() 
        else:
            return Article.objects.filter(author=self.request.user)
        

class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:home')
    template_name = 'registration/article_confirm_delete.html'
    