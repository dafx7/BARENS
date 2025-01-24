import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barens.settings')  # Ganti 'barens' dengan nama project Anda
django.setup()

from main.models import TipeKamar

# Update atau buat ulang data untuk Suite Double
suite_double_data = {
    "nama": "Suite Double",
    "deskripsi": "Kamar nyaman dengan tempat tidur double, tersedia pilihan token dan non-token dengan harga yang sesuai.",
    "fasilitas": "1 bed (6 kaki), toilet duduk, shower + water heater, lemari rak, AC, kamar token dan non-token, TV, meja dan kursi belajar",
    "harga_per_bulan_1_orang": 1800000,  # Harga token
    "harga_non_token": 2000000,  # Harga non-token
    "harga_per_bulan_2_orang": 2000000,
    "jumlah_kamar": 2,
    "max_penghuni": 2
}

tipe_kamar, created = TipeKamar.objects.update_or_create(
    nama=suite_double_data['nama'],  # Gunakan nama sebagai kriteria unik
    defaults={
        "deskripsi": suite_double_data['deskripsi'],
        "fasilitas": suite_double_data['fasilitas'],
        "harga_per_bulan_1_orang": suite_double_data['harga_per_bulan_1_orang'],
        "harga_non_token": suite_double_data['harga_non_token'],
        "harga_per_bulan_2_orang": suite_double_data['harga_per_bulan_2_orang'],
        "jumlah_kamar": suite_double_data['jumlah_kamar'],
        "max_penghuni": suite_double_data['max_penghuni']
    }
)

if created:
    print("Tipe kamar 'Suite Double' berhasil dibuat.")
else:
    print("Tipe kamar 'Suite Double' berhasil diperbarui.")
