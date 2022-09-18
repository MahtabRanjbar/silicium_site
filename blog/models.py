from accounts.models import CustomUser
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone


# managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def published(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='subcateogry')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, )
    status = models.BooleanField(max_length=200, verbose_name='Be visible')
    position = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Categories'

    objects = CategoryManager()


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('i', 'Investigation'),
        ('b', 'Back')
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    slug = models.SlugField(max_length=200, unique=True, )
    category = models.ManyToManyField("blog.category", related_name='article')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='Special Article')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='i')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("accounts:home")

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.published()])
    category_to_str.short_description = 'categories'

    class Meta:
        ordering = ['-published_at']

    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    





