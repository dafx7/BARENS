import os
import django
from django.utils.timezone import now
import calendar
import json

# ✅ Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")
django.setup()

from main.models import CustomUser, Kamar, Pemesanan, TipeKamar
from dashboard.models import Transaksi, StatusPembayaran, MetodePembayaran
from django.test import RequestFactory
from admin_dashboard.views import statistik_penghuni

# ✅ STEP 1: CLEAR OLD TRANSACTION DATA
print("🗑️ Deleting old transactions...")
Transaksi.objects.all().delete()

# ✅ STEP 2: CREATE TEST USERS (if needed)
print("👤 Creating test users...")
user1, _ = CustomUser.objects.get_or_create(username="user1", email="user1@example.com", first_name="Alice")
user2, _ = CustomUser.objects.get_or_create(username="user2", email="user2@example.com", first_name="Bob")

# ✅ STEP 3: CREATE TEST ROOMS
print("🏠 Creating test rooms...")
tipe_kamar, _ = TipeKamar.objects.get_or_create(
    nama="Standard Single",
    deskripsi="1 bed (3 kaki), toilet duduk, lemari rak, AC, shower+water heater, kamar token, TV, meja dan kursi belajar",
    fasilitas="1 bed (3 kaki), toilet duduk, lemari rak, AC, shower+water heater, TV, meja dan kursi belajar",
    harga_per_bulan_1_orang=1400000,  # ✅ Required field
    max_penghuni=1,
    jumlah_kamar=10
)
kamar1, _ = Kamar.objects.get_or_create(tipe_kamar=tipe_kamar, nomor_kamar="STD-001", kapasitas=1)
kamar2, _ = Kamar.objects.get_or_create(tipe_kamar=tipe_kamar, nomor_kamar="STD-002", kapasitas=1)

# ✅ STEP 4: ADD SAMPLE TRANSACTIONS FOR MULTIPLE MONTHS
print("💰 Creating test transactions...")
sample_revenue = {
    "Januari": 25000000,
    "Februari": 22000000,
    "Maret": 25000000,
    "April": 25000000,
    "Mei": 22000000,
    "Juni": 24000000,
    "Juli": 23000000,
    "Agustus": 20000000,
    "September": 25000000,
    "Oktober": 24000000,
    "November": 24000000,
    "Desember": 24000000,
}

tahun_ini = now().year

for month, revenue in sample_revenue.items():
    # ✅ Map Indonesian month names to English
    month_mapping = {
        "Januari": "January", "Februari": "February", "Maret": "March",
        "April": "April", "Mei": "May", "Juni": "June",
        "Juli": "July", "Agustus": "August", "September": "September",
        "Oktober": "October", "November": "November", "Desember": "December"
    }

    # ✅ Convert Indonesian month to English before indexing
    english_month = month_mapping.get(month, None)
    if not english_month:
        raise ValueError(f"Invalid month name: {month}")

    month_number = list(calendar.month_name).index(english_month)  # Convert to number (1-12)

    Transaksi.objects.create(
        user=user1,
        tipe_kamar=kamar1.tipe_kamar,
        tanggal_pembayaran=f"{tahun_ini}-{month_number:02d}-10",  # Format: YYYY-MM-DD
        nominal=revenue,
        metode_pembayaran=MetodePembayaran.BANK_TRANSFER,
        status=StatusPembayaran.LUNAS,
        durasi_bayar=1,
        jenis_durasi="per_bulan",
    )

print("✅ Transactions created successfully.")

# ✅ STEP 5: CALL API & TEST STATISTIK PENDAPATAN
print("📊 Running statistik_penghuni test...")

factory = RequestFactory()
request = factory.get("/admin/statistik/")
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

factory = RequestFactory()
request = factory.get("/admin/statistik/")

# ✅ Simulate an admin user
admin_user, created = CustomUser.objects.get_or_create(
    username="admin",
    defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
)
request.user = admin_user  # Attach user to request

# ✅ Call the view function with the simulated request
response = statistik_penghuni(request)

data = json.loads(response.content)
print("\n📝 FINAL TEST DATA")
import json

print("\n🔍 Expected Revenue Data:")
print(json.dumps(sample_revenue, indent=4))

print("\n📝 Actual Revenue Data from API:")
print(json.dumps(data["pendapatan"], indent=4))

# ✅ STEP 6: ASSERT EXPECTED RESULTS
assert data["pendapatan"] == sample_revenue, "❌ Revenue statistics are incorrect!"
print("\n✅ TEST PASSED: Statistik Pendapatan correctly reflects revenue!")

