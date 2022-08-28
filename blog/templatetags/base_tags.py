from atexit import register

from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    context = {'categories': Category.objects.filter(status=True)}
    return context
