from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pembayaran


@login_required
def status_pembayaran(request):
    pembayaran_terakhir = Pembayaran.objects.filter(user=request.user).order_by('-tanggal_pembayaran').first()

    return render(request, "dashboard/status_pembayaran.html", {
        "pembayaran": pembayaran_terakhir,
    })
