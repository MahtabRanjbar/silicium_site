from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from blog.models import Article, Category


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    queryset = Article.objects.all()
    context_object_name = 'articles'
    template_name = 'registration/adminlte/home.html'