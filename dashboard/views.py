from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Pembayaran, Transaksi
from datetime import datetime  # ✅ Correct import for using datetime.now()


@login_required
def status_pembayaran(request):
    pembayaran_terakhir = Pembayaran.objects.filter(user=request.user).order_by('-tanggal_pembayaran').first()

    return render(request, "dashboard/status_pembayaran.html", {
        "pembayaran": pembayaran_terakhir,
    })


@login_required
def riwayat_transaksi(request):
    transaksi_list = Transaksi.objects.filter(user=request.user).order_by('-tanggal_transaksi')
    paginator = Paginator(transaksi_list, 5)  # 5 transaksi per halaman
    page_number = request.GET.get("page")
    transaksi = paginator.get_page(page_number)

    return render(request, "dashboard/riwayat_transaksi.html", {"transaksi": transaksi})


@login_required
def bukti_transfer(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, id=transaksi_id, user=request.user)

    if transaksi.bukti_transfer:
        return FileResponse(transaksi.bukti_transfer.open(), content_type="image/jpeg")
    else:
        return FileResponse(open("static/main/images/no-image.png", "rb"), content_type="image/png")


@login_required
def upload_bukti(request):
    """Handles proof of payment upload."""
    if request.method == "POST":
        bulan = request.POST.get("bulan")  # User selects only the month
        nominal = request.POST.get("nominal")
        metode_pembayaran = request.POST.get("metode_pembayaran")
        bukti_transfer = request.FILES.get("bukti_transfer")

        current_year = datetime.now().year  # Automatically get the current year
        bulan_tahun = f"{bulan} {current_year}"  # Format as "DESEMBER 2025"

        # Save to database
        transaksi = Transaksi.objects.create(
            user=request.user,
            bulan=bulan_tahun,  # Store as "DESEMBER 2025"
            nominal=nominal,
            metode_pembayaran=metode_pembayaran,
            status="belum_lunas",  # Default status is "Belum Lunas"
            bukti_transfer=bukti_transfer
        )

        messages.success(request, "Bukti pembayaran berhasil diupload. Menunggu verifikasi.")
        return redirect("riwayat_transaksi")

    return render(request, "dashboard/upload_bukti.html")
