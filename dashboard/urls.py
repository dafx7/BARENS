from django.urls import path
from .views import status_pembayaran, riwayat_transaksi, bukti_transfer, upload_bukti, kritik_saran

urlpatterns = [
    path("status-pembayaran/", status_pembayaran, name="status_pembayaran"),
    path("riwayat-transaksi/", riwayat_transaksi, name="riwayat_transaksi"),
    path('bukti-transfer/<int:transaksi_id>/', bukti_transfer, name='bukti_transfer'),
    path("upload-bukti/", upload_bukti, name="upload_bukti"),
    path("kritik-saran/", kritik_saran, name="kritik_saran"),
]
