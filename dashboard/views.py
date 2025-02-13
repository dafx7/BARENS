from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Pembayaran, Transaksi, KritikSaran, StatusPembayaran, StatusValidasi
from django.utils.timezone import now
from datetime import datetime
from .forms import UploadBuktiForm
from decimal import Decimal, InvalidOperation



@login_required
def status_pembayaran(request):
    """
    Fetch the latest due payment for the user.
    """
    pembayaran = Pembayaran.objects.filter(user=request.user).first()
    transaksi_terakhir = Transaksi.objects.filter(user=request.user).order_by('-tanggal_pembayaran').first()

    return render(request, 'dashboard/status_pembayaran.html', {
        'pembayaran': pembayaran,
        'transaksi_terakhir': transaksi_terakhir
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


from main.models import TipeKamar  # ✅ Import TipeKamar

@login_required
def upload_bukti(request):
    if request.method == "POST":
        tanggal_pembayaran = request.POST.get("tanggal_pembayaran", "").strip()
        nominal = request.POST.get("nominal", "").strip()
        metode_pembayaran = request.POST.get("metode_pembayaran", "").strip()
        jenis_pembayaran = request.POST.get("jenis_pembayaran", "").strip()
        bukti_transfer = request.FILES.get("bukti_transfer")
        tipe_kamar_id = request.POST.get("tipe_kamar")  # ✅ Get selected room

        try:
            durasi_bayar = int(request.POST.get("durasi_bayar", 1))
        except ValueError:
            messages.error(request, "Durasi pembayaran harus berupa angka!")
            return redirect("upload_bukti")

        if not all([tanggal_pembayaran, nominal, metode_pembayaran, jenis_pembayaran, durasi_bayar, bukti_transfer, tipe_kamar_id]):
            messages.error(request, "Semua kolom harus diisi!")
            return redirect("upload_bukti")

        # ✅ Parse date
        try:
            tanggal_pembayaran_obj = datetime.strptime(tanggal_pembayaran, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Format tanggal tidak valid!")
            return redirect("upload_bukti")

        # ✅ Convert nominal to Decimal
        try:
            nominal = Decimal(nominal)
        except InvalidOperation:
            messages.error(request, "Nominal pembayaran tidak valid!")
            return redirect("upload_bukti")

        # ✅ Fetch the selected room
        tipe_kamar = TipeKamar.objects.filter(id=tipe_kamar_id).first()
        if not tipe_kamar:
            messages.error(request, "Tipe kamar tidak ditemukan!")
            return redirect("upload_bukti")

        # ✅ Save transaction with the selected room
        transaksi = Transaksi.objects.create(
            user=request.user,
            tipe_kamar=tipe_kamar,  # ✅ Associate transaction with selected room
            tanggal_pembayaran=tanggal_pembayaran_obj,
            nominal=nominal,
            metode_pembayaran=metode_pembayaran,
            jenis_durasi=jenis_pembayaran,
            durasi_bayar=durasi_bayar,
            status=StatusPembayaran.BELUM_LUNAS,
            status_validasi=StatusValidasi.MENUNGGU,
            bukti_transfer=bukti_transfer,
            tanggal_transaksi=now()
        )

        messages.success(request, "Bukti pembayaran berhasil diupload! Menunggu validasi admin.")
        return redirect("status_pembayaran")

    tipe_kamars = TipeKamar.objects.all()  # ✅ Fetch all room types
    return render(request, "dashboard/upload_bukti.html", {"tipe_kamars": tipe_kamars})


@login_required
def kritik_saran(request):
    if request.method == "POST":
        pesan = request.POST.get("pesan")
        if pesan:
            KritikSaran.objects.create(user=request.user, pesan=pesan)
            messages.success(request, "Kritik dan saran anda telah dikirim!")
            return redirect("kritik_saran")

    return render(request, "dashboard/kritik_saran.html")
