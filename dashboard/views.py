from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Pembayaran, Transaksi, KritikSaran
from django.utils.timezone import now
from datetime import datetime
from .forms import UploadBuktiForm


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


@login_required
def upload_bukti(request):
    if request.method == "POST":
        # Get form data
        tanggal_pembayaran = request.POST.get("tanggal_pembayaran")
        nominal = request.POST.get("nominal")
        metode_pembayaran = request.POST.get("metode_pembayaran")
        jenis_pembayaran = request.POST.get("jenis_pembayaran")  # 🔄 Fix this field name
        durasi_bayar = int(request.POST.get("durasi_bayar", 1))  # Default to 1 month
        bukti_transfer = request.FILES.get("bukti_transfer")

        # Ensure required fields are filled
        if not tanggal_pembayaran or not nominal or not metode_pembayaran or not jenis_pembayaran:
            messages.error(request, "Semua kolom harus diisi!")
            return redirect("upload_bukti")

        # Parse tanggal_pembayaran
        from datetime import datetime
        try:
            tanggal_pembayaran_obj = datetime.strptime(tanggal_pembayaran, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Format tanggal tidak valid!")
            return redirect("upload_bukti")

        # Save transaction with jenis_pembayaran
        transaksi = Transaksi.objects.create(
            user=request.user,
            tanggal_pembayaran=tanggal_pembayaran_obj,
            nominal=nominal,
            metode_pembayaran=metode_pembayaran,
            jenis_durasi=jenis_pembayaran,  # 🔄 Fixed field name
            durasi_bayar=durasi_bayar,
            status="BELUM" if not bukti_transfer else "LUNAS",
            bukti_transfer=bukti_transfer,
            tanggal_transaksi=now()
        )

        # Update the due date in Pembayaran model
        pembayaran, created = Pembayaran.objects.get_or_create(user=request.user)
        pembayaran.update_jatuh_tempo(tanggal_pembayaran_obj, durasi_bayar, jenis_pembayaran)  # 🔄 Fixed field name

        messages.success(request, "Bukti pembayaran berhasil diupload!")
        return redirect("upload_bukti")

    return render(request, "dashboard/upload_bukti.html")






@login_required
def kritik_saran(request):
    if request.method == "POST":
        pesan = request.POST.get("pesan")
        if pesan:
            KritikSaran.objects.create(user=request.user, pesan=pesan)
            messages.success(request, "Kritik dan saran anda telah dikirim!")
            return redirect("kritik_saran")

    return render(request, "dashboard/kritik_saran.html")
