from atexit import register
import re

from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    context = {'categories': Category.objects.filter(status=True)}
    return context

@register.inclusion_tag('registration/adminlte/partials/link.html')
def link(request, link_name, content):
    return {
        'request': request,
        'link_name': link_name,
        'link': f"accounts:{link_name}",
        'content': content,
    }
