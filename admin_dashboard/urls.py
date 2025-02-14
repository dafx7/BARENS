from django.urls import path
from .views import (kelola_penghuni, tambah_penghuni, edit_penghuni, hapus_penghuni, pemesanan_kamar,
                    konfirmasi_pemesanan, tolak_pemesanan, validasi_pembayaran, konfirmasi_pembayaran, tolak_pembayaran,
                    kelola_kritik_saran, statistik_page, statistik_penghuni)

urlpatterns = [
    path("pengelolaan-akun/", kelola_penghuni, name="kelola_penghuni"),
    path("tambah-penghuni/", tambah_penghuni, name="tambah_penghuni"),
    path("edit-penghuni/<int:user_id>/", edit_penghuni, name="edit_penghuni"),
    path("hapus-penghuni/<int:user_id>/", hapus_penghuni, name="hapus_penghuni"),
    path('pemesanan/', pemesanan_kamar, name='pemesanan_kamar'),
    path('pemesanan/konfirmasi/<int:pemesanan_id>/', konfirmasi_pemesanan, name='konfirmasi_pemesanan'),
    path('pemesanan/tolak/<int:pemesanan_id>/', tolak_pemesanan, name='tolak_pemesanan'),
    path('validasi-pembayaran/', validasi_pembayaran, name='validasi_pembayaran'),
    path('validasi-pembayaran/konfirmasi/<int:transaksi_id>/', konfirmasi_pembayaran, name='konfirmasi_pembayaran'),
    path('validasi-pembayaran/tolak/<int:transaksi_id>/', tolak_pembayaran, name='tolak_pembayaran'),
    path('kelola-kritik-saran/', kelola_kritik_saran, name='kelola_kritik_saran'),
    path('statistik/', statistik_page, name='statistik_page'),
    path('statistik-penghuni/', statistik_penghuni, name='statistik_penghuni'),
]

