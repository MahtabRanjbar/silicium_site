from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.ArticleList.as_view(), name='home'),
    path('article/create', views.ArticleCreate.as_view(), name='article-create'),
    path('article/update/<int:pk>', views.ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', views.ArticleDelete.as_view(), name='article-delete'),
    path('profile/', views.Profile.as_view(), name='profile'),
    
]

