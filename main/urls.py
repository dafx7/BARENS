from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tipe-kamar/', views.tipe_kamar, name='tipe_kamar'),
    path('form-pemesanan/', views.PemesananView.as_view(), name='form_pemesanan'),
    path('success/', views.SuccessView.as_view(), name='success_page'),
]
