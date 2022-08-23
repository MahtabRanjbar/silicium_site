from msilib.schema import _Validation_records

from django.urls import path

from blog import views

urlpatterns = [
    path('admin/', views.home, name='home'),
]
