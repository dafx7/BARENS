import os
import django

# ✅ Inisialisasi Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")  # Ganti "barens" dengan nama proyek Anda
django.setup()

# ✅ Import model yang digunakan
from main.models import TipeKamar  # Ganti "your_app" dengan nama aplikasi Django Anda


# ✅ Loop untuk mengupdate semua data di dalam database
def update_fasilitas():
    tipe_kamars = TipeKamar.objects.all()  # Ambil semua data dalam tabel TipeKamar

    for tipe_kamar in tipe_kamars:
        if tipe_kamar.fasilitas:  # Pastikan fasilitas tidak kosong/null
            tipe_kamar.fasilitas = tipe_kamar.fasilitas.replace(",", " | ")  # Ganti koma dengan "|"
            tipe_kamar.save()  # Simpan perubahan

    print("✅ Semua fasilitas berhasil diperbarui!")


# ✅ Jalankan fungsi untuk update data
update_fasilitas()
