from django.urls import path
from .views import kelola_penghuni, tambah_penghuni, edit_penghuni, hapus_penghuni, pemesanan_kamar

urlpatterns = [
    path("pengelolaan-akun/", kelola_penghuni, name="kelola_penghuni"),
    path("tambah-penghuni/", tambah_penghuni, name="tambah_penghuni"),
    path("edit-penghuni/<int:user_id>/", edit_penghuni, name="edit_penghuni"),
    path("hapus-penghuni/<int:user_id>/", hapus_penghuni, name="hapus_penghuni"),
    path('pemesanan-kamar/', pemesanan_kamar, name='pemesanan_kamar'),
]
