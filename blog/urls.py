from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>', views.detail_view, name='detail'),
    path('category/<slug:slug>', views.category_view, name='category'),
    path('page/<int:page>', views.home, name='home'),
    
]
