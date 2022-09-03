from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/adminlte/home.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all() 
        else:
            return Article.objects.filter(author=self.reuqest.user)
