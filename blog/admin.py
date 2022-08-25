from django.contrib import admin

from blog.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_at', 'status']
    list_filter = ['published_at', 'status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-published_at']



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'title', 'slug', 'status']
    list_filter = ['status']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}























