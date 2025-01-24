from django.db import models

class TipeKamar(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    fasilitas = models.TextField()
    harga_per_bulan_1_orang = models.DecimalField(max_digits=10, decimal_places=2)
    harga_per_bulan_2_orang = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama


class KamarImage(models.Model):
    tipe_kamar = models.ForeignKey(TipeKamar, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='kamar/')

    def __str__(self):
        return f"Gambar untuk {self.tipe_kamar.nama}"
