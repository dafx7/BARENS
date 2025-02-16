import os
import django

# ✅ Set the settings module BEFORE running django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barens.settings")
django.setup()  # Ensure Django initializes correctly

# ✅ Import Django models AFTER django.setup()
from main.models import CustomUser, Kamar, Pemesanan, TipeKamar
from dashboard.models import Transaksi, StatusPembayaran, MetodePembayaran, Pembayaran
from django.utils.timezone import now
from django.db.models import Sum
from django.test import RequestFactory
from admin_dashboard.views import statistik_penghuni
import json

print("✅ Django environment initialized successfully.")

# ✅ STEP 1: CLEAR ALL OLD DATA (Except TipeKamar)
print("🗑️ Deleting old data...")

CustomUser.objects.all().delete()
Kamar.objects.all().delete()
Pemesanan.objects.all().delete()
Transaksi.objects.all().delete()

print("✅ All user, booking, room, and transaction data deleted.")
print("⚠️ Keeping all TipeKamar data intact.")

# ✅ STEP 2: RETRIEVE EXISTING ROOM TYPES
tipe_kamars = list(TipeKamar.objects.all())
if not tipe_kamars:
    raise Exception("⚠️ No TipeKamar found! Please add room types first.")

# ✅ STEP 3: CREATE TEST USERS
print("👤 Creating test users...")
user1 = CustomUser.objects.create(username="user1", email="user1@example.com", first_name="Alice", is_penghuni=True)
user2 = CustomUser.objects.create(username="user2", email="user2@example.com", first_name="Bob", is_penghuni=True)

# ✅ STEP 4: CREATE KAMAR FROM TIPE_KAMAR DATA
print("🏠 Creating rooms from available TipeKamar...")
existing_numbers = set()  # Track used room numbers

for tipe in tipe_kamars:
    for i in range(1, tipe.jumlah_kamar + 1):
        # Generate a unique room number
        base_name = tipe.nama.replace(" ", "").upper()[:5]  # Take first 5 characters of name
        nomor_kamar = f"{base_name}-{i}"

        # Ensure unique room number
        while nomor_kamar in existing_numbers:
            i += 1
            nomor_kamar = f"{base_name}-{i}"

        # Create the room
        Kamar.objects.create(
            tipe_kamar=tipe,
            nomor_kamar=nomor_kamar,
            kapasitas=tipe.max_penghuni
        )
        existing_numbers.add(nomor_kamar)

print("✅ All rooms created successfully.")

# ✅ STEP 5: ASSIGN USERS TO KAMAR
print("🛏️ Assigning users to rooms...")
kamar_list = list(Kamar.objects.all())  # ✅ Fetch created rooms
kamar_1 = kamar_list[0]
kamar_2 = kamar_list[1]

pemesanan_1 = Pemesanan.objects.create(
    nama=user1.first_name,
    kontak=user1.email,
    kamar=kamar_1,
    tipe_sewa="bulanan",
    durasi=1,
    jumlah_penghuni=1,
    tanggal_mulai=now().date(),
    status="diterima",
    user=user1,
)
kamar_1.penghuni_sekarang = 1
kamar_1.save()

pemesanan_2 = Pemesanan.objects.create(
    nama=user2.first_name,
    kontak=user2.email,
    kamar=kamar_2,
    tipe_sewa="bulanan",
    durasi=1,
    jumlah_penghuni=1,
    tanggal_mulai=now().date(),
    status="diterima",
    user=user2,
)
kamar_2.penghuni_sekarang = 1
kamar_2.save()

print("✅ Users assigned to rooms.")

# ✅ STEP 6: ADD PAYMENT RECORDS
print("💰 Creating test transactions...")

transaksi_1 = Transaksi.objects.create(
    user=user1,
    tipe_kamar=kamar_1.tipe_kamar,
    tanggal_pembayaran=now().date(),
    nominal=1500000,
    metode_pembayaran=MetodePembayaran.BANK_TRANSFER,
    status=StatusPembayaran.LUNAS,
    durasi_bayar=1,
    jenis_durasi="per_bulan",
)

transaksi_2 = Transaksi.objects.create(
    user=user2,
    tipe_kamar=kamar_2.tipe_kamar,
    tanggal_pembayaran=now().date(),
    nominal=1400000,
    metode_pembayaran=MetodePembayaran.E_WALLET,
    status=StatusPembayaran.BELUM_LUNAS,
    durasi_bayar=1,
    jenis_durasi="per_bulan",
)

# ✅ Ensure payment records update due dates
pembayaran_1, _ = Pembayaran.objects.get_or_create(user=user1)
pembayaran_1.update_jatuh_tempo(transaksi_1.tanggal_pembayaran, transaksi_1.durasi_bayar, transaksi_1.jenis_durasi)

pembayaran_2, _ = Pembayaran.objects.get_or_create(user=user2)
pembayaran_2.update_jatuh_tempo(transaksi_2.tanggal_pembayaran, transaksi_2.durasi_bayar, transaksi_2.jenis_durasi)

print("✅ Transactions added.")

# ✅ STEP 7: VALIDATE FINAL STATISTICS
from django.test import RequestFactory
from django.contrib.auth import get_user_model

print("📊 Running statistik_penghuni test...")

factory = RequestFactory()
request = factory.get("/admin/statistik/")

# ✅ Create or retrieve a test admin user
User = get_user_model()
admin_user, created = User.objects.get_or_create(username="admin", is_staff=True, is_superuser=True)
request.user = admin_user  # ✅ Assign authenticated user

# ✅ Call the statistik_penghuni view
response = statistik_penghuni(request)

# ✅ Print JSON response
import json
data = json.loads(response.content)

print("\n📝 FINAL TEST DATA")
print(json.dumps(data, indent=4))

# ✅ Validate Expected Output
assert data["total_penghuni_aktif"] == 2, "❌ Penghuni aktif count is incorrect!"
assert data["pemesanan_kamar"]["terisi"] == 2, "❌ Room occupancy count is incorrect!"
assert data["pemesanan_kamar"]["kosong"] == (sum(t.jumlah_kamar for t in tipe_kamars) - 2), "❌ Room availability count is incorrect!"

print("\n✅ TEST PASSED: Statistics correctly reflect room assignments!")
