from multiprocessing import reduction
from blog.models import Article

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['author', 'title', 'slug', 'category', 'description', 
                           'thumbnail', 'published_at', 'is_special', 'status']

        elif request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'description',
                           'thumbnail', 'is_special', 'published_at']

        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


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
                return redirect('accounts:profile')
        else:
            return redirect('accounts:login')
   
        
class SuperUserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

