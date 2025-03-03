from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class TipeKamar(models.Model):
    nama = models.CharField(max_length=100)
    fasilitas = models.TextField()
    harga_per_bulan_1_orang = models.DecimalField(max_digits=10, decimal_places=2)
    harga_per_bulan_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_per_bulan_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_1_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_penghuni = models.PositiveIntegerField()
    jumlah_kamar = models.PositiveIntegerField()

    def __str__(self):
        return self.nama


class Kamar(models.Model):
    tipe_kamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE, related_name="kamar")
    nomor_kamar = models.CharField(max_length=10, unique=True)
    kapasitas = models.PositiveIntegerField()
    penghuni_sekarang = models.PositiveIntegerField(default=0)

    @property
    def is_full(self):
        return self.penghuni_sekarang >= self.kapasitas

    def tambah_penghuni(self):
        """Increase occupancy if the room is not full."""
        if not self.is_full:
            self.penghuni_sekarang += 1
            self.save()
        else:
            raise ValueError("Kamar sudah penuh!")

    def kurangi_penghuni(self):
        """Decrease occupancy if there are tenants inside."""
        if self.penghuni_sekarang > 0:
            self.penghuni_sekarang -= 1
            self.save()

    def __str__(self):
        return f"Kamar {self.nomor_kamar} ({self.tipe_kamar.nama})"


class KamarImage(models.Model):
    tipe_kamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='kamar/')

    def __str__(self):
        return f"Gambar untuk {self.tipe_kamar.nama}"


class Pemesanan(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu'),
        ('diterima', 'Diterima'),
        ('ditolak', 'Ditolak')
    ]

    nama = models.CharField(max_length=255)
    kontak = models.CharField(max_length=255)
    kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE, related_name="pemesanan")
    tipe_sewa = models.CharField(max_length=10, choices=[('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], default='bulanan')
    durasi = models.PositiveIntegerField(help_text="Durasi dalam jumlah bulan atau tahun")
    jumlah_penghuni = models.PositiveIntegerField()
    tanggal_mulai = models.DateField()
    tanggal_pemesanan = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='menunggu')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='pemesanan', null=True, blank=True)

    def save(self, *args, **kwargs):
        """Auto-update room occupancy when reservation status changes."""
        is_new = self.pk is None  # Check if it's a new instance

        if not is_new:
            previous_status = Pemesanan.objects.filter(pk=self.pk).values_list("status", flat=True).first()
        else:
            previous_status = None  # No previous status if it's new

        super().save(*args, **kwargs)

        # Only update room occupancy when status changes
        if self.status == "diterima" and (is_new or previous_status != "diterima"):
            try:
                self.kamar.tambah_penghuni()
            except ValueError as e:
                print(f"❌ Error: {e}")

        elif self.status == "ditolak" and previous_status == "diterima":
            self.kamar.kurangi_penghuni()

    def __str__(self):
        return f"Pemesanan {self.nama} untuk {self.kamar}"


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_penghuni = models.BooleanField(default=False)
    tanggal_bergabung = models.DateField(null=True, blank=True)
    tanggal_keluar = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "first_name"]  # Hapus "email"

    @property
    def nomor_kamar(self):
        """Mengembalikan nomor kamar dari pemesanan aktif (status diterima)."""
        pemesanan_aktif = self.pemesanan.filter(status="diterima").first()
        return pemesanan_aktif.kamar.nomor_kamar if pemesanan_aktif else "Belum Menempati Kamar"

    def save(self, *args, **kwargs):
        """Auto-set tanggal_keluar when is_penghuni changes to False."""
        if not self.is_penghuni:
            self.tanggal_keluar = now().date()
        elif self.is_penghuni:
            self.tanggal_keluar = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
