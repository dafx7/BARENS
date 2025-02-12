from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tipe-kamar/', views.tipe_kamar, name='tipe_kamar'),
    path('pemesanan/', views.PemesananView.as_view(), name='form_pemesanan'),
    path('get-jumlah-penghuni/<int:tipe_kamar_id>/', views.get_jumlah_penghuni, name='get_jumlah_penghuni'),
    path('success/', views.SuccessView.as_view(), name='success_page'),
    path('lokasi/', views.lokasi, name='lokasi'),
    path('faq/', views.faq, name='faq'),
    path('hubungi-kami/', views.hubungi_kami, name='hubungi_kami'),
    path("login/", auth_views.LoginView.as_view(template_name="main/login.html"), name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("register/", views.register, name="register"),
]
