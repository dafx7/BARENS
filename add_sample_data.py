import os
import django

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barens.settings')  # Ganti 'barens' dengan nama project Anda
django.setup()

from main.models import TipeKamar

# Template deskripsi yang akan digunakan
description_template = """
Kamar nyaman dengan {fasilitas_deskripsi}. Desain yang fungsional dan modern, ideal untuk {orang}.
"""

# Data untuk memperbarui deskripsi
update_data = [
    {
        "nama": "Standard Double",
        "fasilitas_deskripsi": "tempat tidur double (6 kaki), AC, meja kerja, kamar mandi pribadi dengan shower + water heater",
        "orang": "dua orang yang menginginkan kenyamanan dengan harga terjangkau",
    },
    {
        "nama": "Suite Triple",
        "fasilitas_deskripsi": "dua tempat tidur (6 kaki dan 3 kaki), AC, meja kerja, kamar mandi pribadi dengan shower + water heater",
        "orang": "tiga orang yang menginginkan ruang lebih luas dan kenyamanan maksimal",
    },
    {
        "nama": "Standard Single",
        "fasilitas_deskripsi": "tempat tidur single (3 kaki), AC, meja kerja, kamar mandi pribadi dengan shower + water heater",
        "orang": "satu orang yang mencari kenyamanan dengan harga terjangkau",
    },
    {
        "nama": "Suite Double",
        "fasilitas_deskripsi": "tempat tidur double (6 kaki), AC, meja kerja, kamar mandi pribadi dengan shower + water heater",
        "orang": "dua orang yang menginginkan ruang lebih luas dan kenyamanan maksimal",
    },
    {
        "nama": "Standard Twin",
        "fasilitas_deskripsi": "dua tempat tidur single (3 kaki), AC, meja kerja, kamar mandi pribadi dengan shower + water heater",
        "orang": "dua orang yang ingin berbagi ruang dengan kenyamanan",
    },
    {
        "nama": "Standard A",
        "fasilitas_deskripsi": "tempat tidur single (3 kaki), AC, meja kerja, kamar mandi pribadi dengan ember dan gayung",
        "orang": "satu orang yang mencari opsi hemat dengan fasilitas dasar",
    },
    {
        "nama": "Standard B",
        "fasilitas_deskripsi": "tempat tidur kecil (2,5 kaki), kipas angin, meja kerja, dan lemari kayu",
        "orang": "satu orang dengan kebutuhan minimalis",
    },
]

# Update deskripsi berdasarkan data
for data in update_data:
    try:
        kamar = TipeKamar.objects.get(nama=data["nama"])
        kamar.deskripsi = description_template.format(
            fasilitas_deskripsi=data["fasilitas_deskripsi"],
            orang=data["orang"]
        )
        kamar.save()
        print(f"Deskripsi untuk '{kamar.nama}' berhasil diperbarui.")
    except TipeKamar.DoesNotExist:
        print(f"Kamar dengan nama '{data['nama']}' tidak ditemukan di database.")

print("Update deskripsi selesai!")
