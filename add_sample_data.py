import random
from datetime import datetime, timedelta
import django
import os

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")
django.setup()

from main.models import Pemesanan, TipeKamar, CustomUser

# Get all available room types
tipe_kamars = list(TipeKamar.objects.all())

# Get a user to assign (or create a dummy user)
user, created = CustomUser.objects.get_or_create(
    username="testuser",
    defaults={"email": "testuser@example.com", "phone_number": "08123456789", "is_penghuni": False}
)

# Generate 10 new dummy bookings
for i in range(10):
    tipe_kamar = random.choice(tipe_kamars)  # Pick a random room type
    durasi = random.choice([3, 6, 12])  # Durasi dalam bulan
    tipe_sewa = "bulanan" if durasi < 12 else "tahunan"
    jumlah_penghuni = random.randint(1, tipe_kamar.max_penghuni)
    tanggal_mulai = datetime.today().date() + timedelta(days=random.randint(1, 30))

    Pemesanan.objects.create(
        nama=f"User {i+1}",
        kontak=f"0812345678{i}",
        tipe_kamar=tipe_kamar,
        tipe_sewa=tipe_sewa,
        durasi=durasi,
        jumlah_penghuni=jumlah_penghuni,
        tanggal_mulai=tanggal_mulai,
        status="menunggu",
        user=user
    )

print("✅ 10 Pemesanan baru berhasil ditambahkan!")
