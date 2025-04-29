from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class TipeKamar(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    fasilitas = models.TextField()
    harga_per_bulan_1_orang = models.DecimalField(max_digits=10, decimal_places=2)
    harga_per_bulan_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_per_bulan_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_1_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    harga_non_token_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_penghuni = models.PositiveIntegerField()
    jumlah_kamar = models.PositiveIntegerField()

    @property
    def sisa_kamar(self):
        total_pemesanan_diterima = self.pemesanan.filter(status='diterima').count()
        return max(self.jumlah_kamar - total_pemesanan_diterima, 0)

    def __str__(self):
        return self.nama


class Kamar(models.Model):
    LANTAI_CHOICES = [
        (1, "Lantai 1"),
        (2, "Lantai 2"),
        (3, "Lantai 3"),
    ]

    lantai = models.PositiveIntegerField(choices=LANTAI_CHOICES)
    nomor_kamar = models.CharField(max_length=10)
    kapasitas = models.PositiveIntegerField()
    penghuni_sekarang = models.PositiveIntegerField(default=0)

    @property
    def is_full(self):
        return self.penghuni_sekarang >= self.kapasitas


    def tambah_penghuni(self):
        if not self.is_full:
            self.penghuni_sekarang += 1
            self.save()
        else:
            raise ValueError("Kamar sudah penuh!")

    def kurangi_penghuni(self):
        if self.penghuni_sekarang > 0:
            self.penghuni_sekarang -= 1
            self.save()

    class Meta:
        unique_together = ('nomor_kamar', 'lantai')  # Tambahkan ini!

    def __str__(self):
        return f"Kamar {self.nomor_kamar} (Lantai {self.lantai})"


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
    tipe_kamar = models.ForeignKey(TipeKamar, on_delete=models.SET_NULL, related_name='pemesanan', null=True)
    tipe_sewa = models.CharField(max_length=10, choices=[('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], default='bulanan')
    durasi = models.PositiveIntegerField(help_text="Durasi dalam jumlah bulan atau tahun")
    jumlah_penghuni = models.PositiveIntegerField()
    tanggal_mulai = models.DateField()
    tanggal_pemesanan = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='menunggu')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='pemesanan', null=True, blank=True)

    def __str__(self):
        return f"Pemesanan {self.nama} - {self.tipe_kamar.nama if self.tipe_kamar else 'Belum Dipilih'} - Status: {self.status}"



class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_penghuni = models.BooleanField(default=False)
    tanggal_bergabung = models.DateField(null=True, blank=True)
    tanggal_keluar = models.DateField(null=True, blank=True)

    kamar = models.ForeignKey(Kamar, on_delete=models.SET_NULL, null=True, blank=True, related_name='penghuni')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "first_name"]

    @property
    def nomor_kamar(self):
        return self.kamar.nomor_kamar if self.kamar else "Belum Menempati Kamar"

    def save(self, *args, **kwargs):
        if not self.is_penghuni:
            self.tanggal_keluar = now().date()
            self.kamar = None  # Kosongkan kamar jika bukan penghuni
        elif self.is_penghuni and not self.tanggal_bergabung:
            self.tanggal_bergabung = now().date()
            self.tanggal_keluar = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

