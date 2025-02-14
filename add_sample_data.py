import random
from datetime import datetime, timedelta
import django
import os

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")
django.setup()

from dashboard.models import KritikSaran
from django.contrib.auth import get_user_model

User = get_user_model()

# Get all users (or create a dummy user if none exists)
users = list(User.objects.all())

if not users:
    user, created = User.objects.get_or_create(
        username="testuser",
        defaults={"email": "testuser@example.com", "phone_number": "08123456789", "is_penghuni": False}
    )
    users = [user]

# List of random Kritik & Saran messages
kritik_messages = [
    "Pelayanan sangat baik! Terima kasih.",
    "Harap lebih meningkatkan kebersihan kamar.",
    "WiFi kadang lambat, bisa diperbaiki?",
    "Fasilitas sudah cukup bagus, tapi bisa lebih baik lagi.",
    "Mohon ada lebih banyak opsi pembayaran.",
    "Staf sangat ramah dan membantu! 👍",
    "Mohon ada lebih banyak event komunitas penghuni.",
    "Keamanan gedung perlu ditingkatkan lagi.",
    "Saran: bisa ada aplikasi mobile untuk penghuni?",
    "Tolong perbaiki AC di beberapa kamar."
]

# Generate 10 random Kritik & Saran
for i in range(10):
    user = random.choice(users)  # Pick a random user
    pesan = random.choice(kritik_messages)  # Pick a random message
    tanggal_dikirim = datetime.today() - timedelta(days=random.randint(1, 30))  # Random past date

    KritikSaran.objects.create(
        user=user,
        pesan=pesan,
        tanggal_dikirim=tanggal_dikirim
    )

print("✅ 10 Kritik & Saran berhasil ditambahkan!")
