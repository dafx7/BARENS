from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Status Pembayaran Enum
class StatusPembayaran(models.TextChoices):
    LUNAS = "LUNAS", "Lunas"
    BELUM_LUNAS = "BELUM", "Belum Lunas"

# Metode Pembayaran Enum
class MetodePembayaran(models.TextChoices):
    BANK_TRANSFER = "bank_transfer", "Transfer Bank"
    E_WALLET = "e_wallet", "E-Wallet"

class Pembayaran(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pembayaran")
    tanggal_pembayaran = models.DateField(verbose_name="Tanggal Pembayaran")
    jumlah_pembayaran = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jumlah Pembayaran")
    status = models.CharField(
        max_length=10,
        choices=StatusPembayaran.choices,
        default=StatusPembayaran.BELUM_LUNAS,
        verbose_name="Status Pembayaran"
    )
    jatuh_tempo_berikutnya = models.DateField(verbose_name="Jatuh Tempo Berikutnya")

    class Meta:
        verbose_name = "Pembayaran"
        verbose_name_plural = "Pembayaran"

    def __str__(self):
        return f"Pembayaran {self.user.username} - {self.status}"


class Transaksi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaksi")
    bulan = models.CharField(max_length=13, verbose_name="Bulan")  # Contoh: "JANUARI 2025"
    nominal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Nominal Pembayaran")
    metode_pembayaran = models.CharField(
        max_length=20,
        choices=MetodePembayaran.choices,
        verbose_name="Metode Pembayaran"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusPembayaran.choices,
        default=StatusPembayaran.BELUM_LUNAS,
        verbose_name="Status Pembayaran"
    )
    bukti_transfer = models.ImageField(
        upload_to="bukti_transfer/",
        null=True,
        blank=True,
        verbose_name="Bukti Transfer"
    )
    tanggal_transaksi = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Transaksi")

    class Meta:
        verbose_name = "Riwayat Transaksi"
        verbose_name_plural = "Riwayat Transaksi"

    def __str__(self):
        return f"{self.bulan} - {self.user.username}"
