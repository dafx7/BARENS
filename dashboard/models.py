from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

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
    """ Track user's next due date based on last payment. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pembayaran")
    jatuh_tempo = models.DateField(verbose_name="Jatuh Tempo Berikutnya", null=True, blank=True)

    def update_jatuh_tempo(self, tanggal_pembayaran, durasi_bayar, jenis_durasi):
        """
        Update the due date every time a transaction is made.
        """
        if isinstance(tanggal_pembayaran, date):
            tanggal_pembayaran = tanggal_pembayaran
        else:
            tanggal_pembayaran = tanggal_pembayaran.date()  # Convert datetime to date

        # If jatuh_tempo is None or past, set it to transaction date
        if not self.jatuh_tempo or self.jatuh_tempo < tanggal_pembayaran:
            self.jatuh_tempo = tanggal_pembayaran

        # Handle per month and per year manually
        if jenis_durasi == "per_bulan":
            for _ in range(durasi_bayar):
                if self.jatuh_tempo.month == 12:
                    self.jatuh_tempo = date(self.jatuh_tempo.year + 1, 1, self.jatuh_tempo.day)
                else:
                    self.jatuh_tempo = date(self.jatuh_tempo.year, self.jatuh_tempo.month + 1, self.jatuh_tempo.day)

        elif jenis_durasi == "per_tahun":
            self.jatuh_tempo = date(self.jatuh_tempo.year + durasi_bayar, self.jatuh_tempo.month, self.jatuh_tempo.day)

        self.save()


class Transaksi(models.Model):
    """ Log every payment transaction """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaksi")
    tanggal_pembayaran = models.DateField(verbose_name="Tanggal Pembayaran")
    nominal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Nominal Pembayaran")
    metode_pembayaran = models.CharField(
        max_length=20,
        choices=MetodePembayaran.choices,
        verbose_name="Metode Pembayaran"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusPembayaran.choices,
        default=StatusPembayaran.LUNAS,
        verbose_name="Status Pembayaran"
    )
    bukti_transfer = models.ImageField(
        upload_to="bukti_transfer/",
        null=True,
        blank=True,
        verbose_name="Bukti Transfer"
    )
    tanggal_transaksi = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Transaksi")

    # ✅ Durasi pembayaran field
    durasi_bayar = models.PositiveIntegerField(verbose_name="Durasi Bayar (Bulan)", default=1)
    jenis_durasi = models.CharField(
        max_length=10,
        choices=[("per_bulan", "Per Bulan"), ("per_tahun", "Per Tahun")],
        verbose_name="Jenis Durasi Pembayaran"
    )

    class Meta:
        verbose_name = "Riwayat Transaksi"
        verbose_name_plural = "Riwayat Transaksi"

    def __str__(self):
        return f"{self.tanggal_pembayaran} - {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Every time a user uploads a new transaction, update 'Pembayaran.jatuh_tempo'.
        """
        super().save(*args, **kwargs)  # Save the transaction first

        # Ensure user has a 'Pembayaran' record, or create one
        pembayaran, created = Pembayaran.objects.get_or_create(user=self.user)

        # ✅ Pass `jenis_durasi` explicitly
        pembayaran.update_jatuh_tempo(self.tanggal_pembayaran, self.durasi_bayar, self.jenis_durasi)




class KritikSaran(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kritik_saran")
    pesan = models.TextField()
    tanggal_dikirim = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kritik dari {self.user.username} - {self.tanggal_dikirim.strftime('%d %B %Y')}"
