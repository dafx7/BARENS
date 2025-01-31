from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission


class TipeKamar(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    fasilitas = models.TextField()
    harga_per_bulan_1_orang = models.DecimalField(max_digits=10, decimal_places=2)  # Harga token 1 orang
    harga_per_bulan_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Harga token 2 orang
    harga_per_bulan_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Harga token 3 orang
    harga_non_token_1_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Harga non-token 1 orang
    harga_non_token_2_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Harga non-token 2 orang
    harga_non_token_3_orang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Harga non-token 3 orang
    max_penghuni = models.PositiveIntegerField()  # Maksimum penghuni
    jumlah_kamar = models.PositiveIntegerField()  # Jumlah kamar tersedia

    def __str__(self):
        return self.nama


    def hitung_harga_tambah_orang(self, jumlah_penghuni):
        """
        Menghitung harga berdasarkan jumlah penghuni.
        Tambahan 200k/orang jika jumlah penghuni melebihi 1.
        """
        if jumlah_penghuni > self.max_penghuni:
            raise ValueError("Jumlah penghuni melebihi kapasitas maksimal.")

        if jumlah_penghuni == 1:
            return self.harga_per_bulan_1_orang
        elif jumlah_penghuni == 2:
            return self.harga_per_bulan_2_orang or self.harga_per_bulan_1_orang + 200000
        elif jumlah_penghuni == 3 and self.max_penghuni == 3:
            return self.harga_per_bulan_3_orang or self.harga_per_bulan_2_orang + 200000

        raise ValueError("Jumlah penghuni tidak valid untuk tipe kamar ini.")


class KamarImage(models.Model):
    tipe_kamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='kamar/')

    def __str__(self):
        return f"Gambar untuk {self.tipe_kamar.nama}"


class Pemesanan(models.Model):
    nama = models.CharField(max_length=255)
    kontak = models.CharField(max_length=255)
    tipe_kamar = models.ForeignKey('TipeKamar', on_delete=models.CASCADE, related_name='pemesanan')
    durasi = models.CharField(max_length=50, choices=[('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')])
    jumlah_penghuni = models.PositiveIntegerField()
    tanggal_mulai = models.DateField()
    tanggal_pemesanan = models.DateTimeField(default=now)

    def __str__(self):
        return f"Pemesanan oleh {self.nama} untuk {self.tipe_kamar.nama}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Gunakan email sebagai identifier utama
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "username"  # Kembali pakai username untuk login
    REQUIRED_FIELDS = ["email", "phone_number", "first_name"]  # Nama lengkap tetap wajib

    def __str__(self):
        return self.username  # Tampilkan username sebagai identifier utama
