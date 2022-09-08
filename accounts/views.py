from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import ProfileForm
from accounts.mixins import (AuthorAccessMixin, FieldsMixin,
                             SuperUserAccessMixin)
from accounts.models import CustomUser


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

    success_url = 'accounts:home'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, UpdateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status' ]
    template_name = 'registration/adminlte/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:home')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'registration/adminlte/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:home")

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self) -> str:
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("accounts:home")
        else:
            return reverse_lazy('accounts:profile')
