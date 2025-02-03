from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Pembayaran, Transaksi


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
