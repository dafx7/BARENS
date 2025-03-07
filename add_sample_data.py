import os
import django

# Konfigurasi Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")
django.setup()

from main.models import Kamar

# Data kamar berdasarkan lantai
kamar_data = {
    1: list(range(101, 113)),  # Lantai 1: 101-112
    2: list(range(1, 12)) + list(range(201, 213)) + list(range(214, 219)),  # Lantai 2
    3: list(range(1, 13)) + list(range(14, 32)),  # Lantai 3
}

# Kapasitas default kamar (ubah sesuai kebutuhan)
DEFAULT_KAPASITAS = 2

# Fungsi untuk menambahkan kamar ke database
def populate_kamar():
    for lantai, nomor_kamar_list in kamar_data.items():
        for nomor_kamar in nomor_kamar_list:
            nomor_kamar_str = str(nomor_kamar)  # Konversi ke string

            # Cek apakah kamar sudah ada di database
            if not Kamar.objects.filter(nomor_kamar=nomor_kamar_str, lantai=lantai).exists():
                Kamar.objects.create(
                    lantai=lantai,
                    nomor_kamar=nomor_kamar_str,
                    kapasitas=DEFAULT_KAPASITAS,
                    penghuni_sekarang=0
                )
                print(f"✅ Kamar {nomor_kamar_str} (Lantai {lantai}) berhasil ditambahkan.")
            else:
                print(f"⚠ Kamar {nomor_kamar_str} (Lantai {lantai}) sudah ada, dilewati.")

if __name__ == "__main__":
    populate_kamar()
