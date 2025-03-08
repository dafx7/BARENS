import os
import django

# Konfigurasi Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")  # Sesuaikan dengan nama proyek Anda
django.setup()

from main.models import TipeKamar  # Sesuaikan dengan nama aplikasi Django Anda

# Data tipe kamar dengan harga dan fasilitas
data_kamar = [
    {
        "nama": "Standard double",
        "fasilitas": "1 bed (6 kaki) | toilet duduk | lemari rak | AC | shower & water heater (tidak ada ember gayung) | kamar token | TV | meja dan kursi belajar",
        "harga_per_bulan_1_orang": 1500000,
        "harga_per_bulan_2_orang": 1500000,
        "max_penghuni": 2,
        "jumlah_kamar": 15
    },
    {
        "nama": "Suite triple",
        "fasilitas": "2 bed (6 kaki dan 3 kaki) | toilet duduk | lemari rak | AC | shower & water heater (tidak ada ember gayung) | kamar non-token | TV | meja dan kursi belajar",
        "harga_per_bulan_3_orang": 2500000,
        "max_penghuni": 3,
        "jumlah_kamar": 3
    },
    {
        "nama": "Standard single",
        "fasilitas": "1 bed (3 kaki) | toilet duduk | lemari rak | AC | shower & water heater (tidak ada ember gayung) | kamar token | TV | meja dan kursi belajar",
        "harga_per_bulan_1_orang": 1400000,
        "max_penghuni": 1,
        "jumlah_kamar": 18
    },
    {
        "nama": "Suite double",
        "fasilitas": "1 bed (6 kaki) | toilet duduk | shower & water heater (tidak ada ember gayung) | lemari rak | AC | kamar token dan non-token | TV | meja dan kursi belajar",
        "harga_per_bulan_2_orang": 1800000,
        "harga_non_token_2_orang": 2000000,
        "max_penghuni": 2,
        "jumlah_kamar": 2
    },
    {
        "nama": "Standard twin",
        "fasilitas": "2 bed (3 kaki) | toilet duduk | lemari rak | AC | shower & water heater (tidak ada ember gayung) | kamar token | TV | meja dan kursi belajar",
        "harga_per_bulan_2_orang": 1700000,
        "max_penghuni": 2,
        "jumlah_kamar": 1
    },
    {
        "nama": "Standard A",
        "fasilitas": "1 bed (3 kaki) | lemari kayu | toilet jongkok | AC | ember+gayung (tidak ada water heater) | kamar token | TV | meja dan kursi belajar",
        "harga_per_bulan_1_orang": 1300000,
        "max_penghuni": 1,
        "jumlah_kamar": 11
    },
    {
        "nama": "Standard B",
        "fasilitas": "1 bed (2,5 kaki) | kipas angin | lemari kayu | meja belajar | meja dan kursi belajar | toilet duduk | kamar token dan non-token",
        "harga_per_bulan_1_orang": 800000,
        "harga_non_token_1_orang": 900000,
        "max_penghuni": 1,
        "jumlah_kamar": 28
    },
]

# Masukkan data ke dalam database
for kamar in data_kamar:
    # Pastikan harga_per_bulan_1_orang memiliki nilai default jika tidak ada
    harga_per_bulan_1_orang = kamar.get("harga_per_bulan_1_orang", 0)
    harga_per_bulan_2_orang = kamar.get("harga_per_bulan_2_orang")
    harga_per_bulan_3_orang = kamar.get("harga_per_bulan_3_orang")
    harga_non_token_1_orang = kamar.get("harga_non_token_1_orang")
    harga_non_token_2_orang = kamar.get("harga_non_token_2_orang")
    harga_non_token_3_orang = kamar.get("harga_non_token_3_orang")

    # Buat atau update data kamar
    TipeKamar.objects.update_or_create(
        nama=kamar["nama"],
        defaults={
            "fasilitas": kamar["fasilitas"],
            "harga_per_bulan_1_orang": harga_per_bulan_1_orang,
            "harga_per_bulan_2_orang": harga_per_bulan_2_orang,
            "harga_per_bulan_3_orang": harga_per_bulan_3_orang,
            "harga_non_token_1_orang": harga_non_token_1_orang,
            "harga_non_token_2_orang": harga_non_token_2_orang,
            "harga_non_token_3_orang": harga_non_token_3_orang,
            "max_penghuni": kamar["max_penghuni"],
            "jumlah_kamar": kamar["jumlah_kamar"]
        }
    )

print("✅ Data berhasil dimasukkan atau diperbarui ke dalam database!")
