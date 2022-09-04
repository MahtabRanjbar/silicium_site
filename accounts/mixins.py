from django.db import models
from django.http import Http404


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
