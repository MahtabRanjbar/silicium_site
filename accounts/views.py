from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.forms import ProfileForm
from accounts.mixins import (AuthorAccessMixin, AuthorsAccessMixin,
                             FieldsMixin, FormValidMixin, SuperUserAccessMixin)
from accounts.models import CustomUser


# Create your views here.
class ArticleList(AuthorsAccessMixin, ListView):
    context_object_name = 'articles'
    template_name = 'registration/adminlte/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'status']
    template_name = 'registration/adminlte/article-create-update.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
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

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

    def get_success_url(self) -> str:
        if self.request.user.is_superuser or self.request.user.is_author:
            return reverse_lazy('accounts:home')
        else:
            return reverse_lazy("accounts:profile")


class Login(LoginView):
    def get_success_url(self) -> str:
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("accounts:home")
        else:
            return reverse_lazy('accounts:profile')
  
        
class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('accounts:password-change-done')
    template_name = 'registration/password_change.html'
