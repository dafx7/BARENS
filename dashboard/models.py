from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class Pembayaran(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pembayaran")
    tanggal_pembayaran = models.DateField()
    jumlah_pembayaran = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[("LUNAS", "Lunas"), ("BELUM", "Belum Lunas")],
        default="BELUM",
    )
    jatuh_tempo_berikutnya = models.DateField()

    def __str__(self):
        return f"Pembayaran {self.user.username} - {self.status}"

