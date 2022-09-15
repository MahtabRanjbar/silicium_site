from django.contrib import admin

from blog.models import Article, Category, IPAddress


admin.site.register(IPAddress)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published_at', 'status','is_special', 'category_to_str']
    list_filter = ['published_at', 'status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-published_at']
    actions = ['make_draft', 'make_published']

    @admin.action(description='Mark selected stories as draft')
    def make_draft(self, request, queryset):
        row_updated = queryset.update(status="d")
        if row_updated == 1:
            message = '1 sotry was'
        else:
            message = f"{row_updated} story were"
        self.message_user(request, f"{message} successfully marked as draft")

    @admin.action(description='Mark selected stories as published')
    def make_published(self, request, queryset):
        row_updated = queryset.update(status="p")
        if row_updated == 1:
            message = '1 sotry was'
        else:
            message = f"{row_updated} story were"
        self.message_user(request, f"{message} successfully marked as published")




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'title', 'slug', 'parent', 'status']
    list_filter = ['status']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    
























