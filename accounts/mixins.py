from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from blog.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['author', 'title', 'slug', 'category', 'description',
                           'thumbnail', 'published_at', 'status' ]
            
        elif request.user.is_author:
            self.fields = ['title', 'slug', 'category', 'description',
                           'thumbnail', 'published_at']
        
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    

class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == (request.user and article.status == "d") or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
    
        
class SuperUserAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
        
