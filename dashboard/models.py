from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta, date
import calendar

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
        Update `jatuh_tempo` based on the latest transaction.
        Ensures correct calculation of due date.
        """

        # ✅ Step 1: Determine the Correct Base Date
        if self.jatuh_tempo and self.jatuh_tempo > tanggal_pembayaran:
            base_date = self.jatuh_tempo  # Use the previous due date
        else:
            base_date = tanggal_pembayaran  # Use the new payment date
        print(base_date)
        # ✅ Step 2: Add Duration Based on Type (Month or Year)
        if jenis_durasi == "per_bulan":
            new_month = (base_date.month - 1 + durasi_bayar) % 12 + 1  # Correct month calculation
            new_year = base_date.year + (base_date.month - 1 + durasi_bayar) // 12

            # Adjust for last day of month
            last_day = calendar.monthrange(new_year, new_month)[1]
            new_day = min(base_date.day, last_day)

            self.jatuh_tempo = date(new_year, new_month, new_day)

        elif jenis_durasi == "per_tahun":
            try:
                self.jatuh_tempo = base_date.replace(year=base_date.year + durasi_bayar)
            except ValueError:
                # Handle leap year issues
                self.jatuh_tempo = base_date.replace(year=base_date.year + durasi_bayar, day=28)
            print("New due date: ", self.jatuh_tempo)
        # ✅ Step 3: Save the Updated Due Date
        self.save()



class StatusValidasi(models.TextChoices):
    MENUNGGU = "menunggu", "Menunggu"
    DITERIMA = "diterima", "Diterima"
    DITOLAK = "ditolak", "Ditolak"

class Transaksi(models.Model):
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
        default=StatusPembayaran.BELUM_LUNAS,  # Default to Belum Lunas
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

    # ✅ New field for validation status
    status_validasi = models.CharField(
        max_length=10,
        choices=StatusValidasi.choices,
        default=StatusValidasi.MENUNGGU,
        verbose_name="Status Validasi Pembayaran"
    )

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
