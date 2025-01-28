from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tipe-kamar/', views.tipe_kamar, name='tipe_kamar'),
    path('form-pemesanan/', views.PemesananView.as_view(), name='form_pemesanan'),
    path('success/', views.SuccessView.as_view(), name='success_page'),
    path('lokasi/', views.lokasi, name='lokasi'),
    path('faq/', views.faq, name='faq'),
    path('hubungi-kami/', views.hubungi_kami, name='hubungi_kami'),
]
