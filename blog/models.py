from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, )
    status = models.BooleanField(max_length=200, verbose_name='Be visible')
    position = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Categories'


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, )
    category = models.ManyToManyField("blog.category")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title