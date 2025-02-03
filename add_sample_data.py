import os
import django
import random
from datetime import timedelta
from django.utils.timezone import now

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barens.settings')  # Change 'barens' to your project name
django.setup()

from dashboard.models import Transaksi
from django.contrib.auth import get_user_model

User = get_user_model()


def create_transactions():
    """Create 10 sample transactions for the first user."""

    user = User.objects.first()  # Get first user in database

    if not user:
        print("❌ No users found. Please create a user first!")
        return

    # Sample transaction data
    months = [
        "JANUARI 2024", "FEBRUARI 2024", "MARET 2024",
        "APRIL 2024", "MEI 2024", "JUNI 2024",
        "JULI 2024", "AGUSTUS 2024", "SEPTEMBER 2024",
        "OKTOBER 2024"
    ]
    payment_methods = ["bank_transfer", "e_wallet"]
    statuses = ["lunas", "belum_lunas"]

    transactions = []

    for i in range(10):
        transaksi = Transaksi(
            user=user,
            bulan=months[i],  # Assign month sequentially
            nominal=random.randint(800000, 3000000),  # Random nominal between 800k - 3M
            metode_pembayaran=random.choice(payment_methods),
            status=random.choice(statuses),
            bukti_transfer=None,  # Change if you want to add real images
            tanggal_transaksi=now() - timedelta(days=random.randint(1, 365))  # Random past date
        )
        transactions.append(transaksi)

    # Bulk create for efficiency
    Transaksi.objects.bulk_create(transactions)

    print("✅ 10 transactions successfully added!")


if __name__ == "__main__":
    create_transactions()
