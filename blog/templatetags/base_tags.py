from atexit import register
from datetime import datetime, timedelta

from django import template
from django.db.models import Count, Q

from ..models import Article, Category

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


@register.inclusion_tag("blog/partials/popular_articles.html")
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)

    return {"popular_articles": Article.objects.published().annotate(
        count=Count("hits", filter=Q(articlehit__created_at__gt=last_month))
        ).order_by('-count', '-published_at')
    }
