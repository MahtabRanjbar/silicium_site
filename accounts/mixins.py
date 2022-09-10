
from blog.models import Article
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['title', 'slug', 'category', 'description', 'thumbnail', 'published_at', 'is_special', 'status']
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)
    

class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if (article.author == request.user and article.status in ['d', 'b']) or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy('accounts:profile'))
        else:
            return redirect(reverse_lazy('accounts:login'))
   
        
class SuperUserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

