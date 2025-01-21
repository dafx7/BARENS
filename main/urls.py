from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL untuk halaman beranda
]
