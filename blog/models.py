from django.db import models
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


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, )
    category = models.ManyToManyField("blog.category", related_name='article')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']

    objects = ArticleManager()
