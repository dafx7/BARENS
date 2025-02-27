from textwrap import indent
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from main.models import CustomUser, Pemesanan, TipeKamar, Kamar
from dashboard.models import Transaksi, StatusValidasi, KritikSaran, StatusPembayaran
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.utils.timezone import now
import calendar
from django.db.models import Case, When, Value, IntegerField


# Fungsi untuk membatasi akses hanya untuk admin
def is_admin(user):
    return user.is_staff  # Hanya admin yang bisa mengakses


@login_required
@user_passes_test(is_admin)
def kelola_penghuni(request):
    """
    Menampilkan daftar penghuni dengan pagination dan fitur pencarian.
    """
    query = request.GET.get("search", "").strip()

    # Filter penghuni berdasarkan pencarian
    if query:
        penghuni_list = CustomUser.objects.filter(
            first_name__icontains=query
        ) | CustomUser.objects.filter(
            email__icontains=query
        )
    else:
        penghuni_list = CustomUser.objects.all().order_by('-id')

    # Pagination (5 penghuni per halaman)
    paginator = Paginator(penghuni_list, 5)
    page_number = request.GET.get("page")
    penghuni = paginator.get_page(page_number)

    return render(request, "admin_dashboard/pengelolaan_akun.html", {
        "penghuni": penghuni,
        "paginator": paginator,
        "query": query,
    })



@login_required
@user_passes_test(is_admin)
def tambah_penghuni(request):
    if request.method == "POST":
        nama_lengkap = (request.POST.get("nama_lengkap") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone_number = (request.POST.get("phone_number") or "").strip()
        is_penghuni = request.POST.get("is_penghuni") == "on"

        # Cek apakah field kosong
        if not nama_lengkap or not email or not phone_number:
            messages.error(request, "Semua field wajib diisi!")
            return redirect("kelola_penghuni")

        # Validasi apakah email sudah digunakan
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan!")
            return redirect("kelola_penghuni")

        # Buat akun penghuni baru
        user = CustomUser.objects.create(
            username=email.split("@")[0],  # Tetap gunakan username dari email
            email=email,
            phone_number=phone_number,
            first_name=nama_lengkap,  # Simpan Nama Lengkap di field first_name
            is_penghuni=is_penghuni,
            tanggal_bergabung=now().date() if is_penghuni else None,
        )
        user.set_password("password123")  # Password default
        user.save()

        messages.success(request, "Akun penghuni berhasil ditambahkan!")
        return redirect("kelola_penghuni")

    return redirect("kelola_penghuni")


@login_required
@user_passes_test(is_admin)
def edit_penghuni(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Ambil daftar semua kamar yang tersedia
    kamar_list = Kamar.objects.all()

    # Cek apakah user sudah memiliki pemesanan aktif
    pemesanan_aktif = user.pemesanan.filter(status="diterima").first()
    kamar_terpilih = pemesanan_aktif.kamar.id if pemesanan_aktif else None

    if request.method == "POST":
        user.username = (request.POST.get("nama") or "").strip()
        user.email = (request.POST.get("email") or "").strip()
        user.phone_number = (request.POST.get("phone_number") or "").strip()
        user.is_penghuni = request.POST.get("is_penghuni") == "on"

        if not user.username or not user.email or not user.phone_number:
            messages.error(request, "Semua field wajib diisi!")
            return redirect("edit_penghuni", user_id=user.id)

        # Update kamar penghuni jika ada perubahan
        nomor_kamar_baru = request.POST.get("nomor_kamar")
        if nomor_kamar_baru:
            kamar_baru = get_object_or_404(Kamar, id=nomor_kamar_baru)

            # Jika ada pemesanan sebelumnya, update pemesanan
            if pemesanan_aktif:
                pemesanan_aktif.kamar = kamar_baru
                pemesanan_aktif.save()
            else:
                # Buat pemesanan baru jika sebelumnya tidak ada
                Pemesanan.objects.create(
                    user=user,
                    kamar=kamar_baru,
                    status="diterima",
                    nama=user.username,
                    kontak=user.phone_number,
                    tipe_sewa="bulanan",
                    durasi=1,  # Default 1 bulan
                    jumlah_penghuni=1,
                    tanggal_mulai=now().date(),
                )

        user.save()
        messages.success(request, "Data penghuni berhasil diperbarui!")

        return redirect("kelola_penghuni")

    return render(request, "admin_dashboard/edit_penghuni.html", {
        "user": user,
        "kamar_list": kamar_list,
        "kamar_terpilih": kamar_terpilih
    })



@login_required
@user_passes_test(is_admin)
def hapus_penghuni(request, user_id):
    """
    Menghapus akun penghuni dengan mencatat tanggal keluar.
    """
    user = get_object_or_404(CustomUser, id=user_id)

    # ✅ Set tanggal_keluar sebelum menghapus
    user.tanggal_keluar = now().date()
    user.save()

    # ✅ Remove is_penghuni status
    user.is_penghuni = False
    user.save()

    # ✅ OPTIONAL: Delete user after recording exit (if required)
    user.delete()

    messages.success(request, "Akun penghuni berhasil dihapus!")
    return redirect("kelola_penghuni")



@login_required
@user_passes_test(is_admin)
def pemesanan_kamar(request):
    # Filter hanya pemesanan yang belum diproses (status "menunggu") dan urutkan dari yang paling lama
    pemesanan_list = Pemesanan.objects.filter(status="menunggu").order_by('tanggal_pemesanan')

    # Tambahkan juga pemesanan yang sudah diproses di bawah daftar yang masih menunggu
    pemesanan_diproses = Pemesanan.objects.exclude(status="menunggu").order_by('-tanggal_pemesanan')

    # Gabungkan hasil query
    pemesanan_list = list(pemesanan_list) + list(pemesanan_diproses)

    # PAGINATION: Batasi 7 pemesanan per halaman
    paginator = Paginator(pemesanan_list, 7)
    page_number = request.GET.get('page')
    pemesanan_page = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/pemesanan_kamar.html', {'pemesanan': pemesanan_page})


@login_required
@user_passes_test(is_admin)
def konfirmasi_pemesanan(request, pemesanan_id):
    pemesanan = get_object_or_404(Pemesanan, id=pemesanan_id)

    if pemesanan.status == 'menunggu':
        pemesanan.status = 'diterima'
        if pemesanan.user:  # Jika pemesanan memiliki akun user yang terhubung
            pemesanan.user.is_penghuni = True
            if not pemesanan.user.tanggal_bergabung:  # ✅ Only set if not already set
                pemesanan.user.tanggal_bergabung = now().date()
            pemesanan.user.save()
        pemesanan.save()
        messages.success(request, f"Pemesanan {pemesanan.nama} telah dikonfirmasi.")

    return redirect('pemesanan_kamar')


@login_required
@user_passes_test(is_admin)
def tolak_pemesanan(request, pemesanan_id):
    pemesanan = get_object_or_404(Pemesanan, id=pemesanan_id)

    if pemesanan.status == 'menunggu':
        pemesanan.status = 'ditolak'
        pemesanan.save()
        messages.error(request, f"Pemesanan {pemesanan.nama} telah ditolak.")

    return redirect('pemesanan_kamar')


@login_required
@user_passes_test(is_admin)
def validasi_pembayaran(request):
    search_query = request.GET.get("search", "").strip()

    # Filter transactions: only MENUNGGU & DITERIMA (excluding DITOLAK)
    transaksi_list = Transaksi.objects.filter(status_validasi__in=["menunggu", "diterima"]).annotate(
        status_order=Case(
            When(status_validasi="menunggu", then=Value(1)),
            When(status_validasi="diterima", then=Value(2)),  # DITOLAK is removed
            output_field=IntegerField()
        )
    ).order_by("status_order", "-tanggal_transaksi")

    # Apply search filter if an input is provided
    if search_query:
        transaksi_list = transaksi_list.filter(user__first_name__icontains=search_query)

    # Pagination (7 transactions per page)
    paginator = Paginator(transaksi_list, 7)
    page_number = request.GET.get("page")
    transaksi = paginator.get_page(page_number)

    return render(
        request,
        "admin_dashboard/pembayaran_validasi.html",
        {"transaksi": transaksi, "search_query": search_query}
    )


@login_required
@user_passes_test(is_admin)
def konfirmasi_pembayaran(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    transaksi.approve_payment()

    messages.success(request, f"Pembayaran {transaksi.user.username} telah divalidasi dan jatuh tempo diperbarui.")
    return redirect('validasi_pembayaran')


@login_required
@user_passes_test(is_admin)
def tolak_pembayaran(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    transaksi.reject_payment()

    messages.warning(request, f"Pembayaran {transaksi.user.username} telah ditolak.")
    return redirect('validasi_pembayaran')


@login_required
@user_passes_test(is_admin)
def kelola_kritik_saran(request):
    # ✅ Fetch all user feedback
    kritik_list = KritikSaran.objects.all().order_by("-tanggal_dikirim")

    # ✅ Implement pagination (7 feedback per page)
    paginator = Paginator(kritik_list, 7)
    page_number = request.GET.get("page")
    kritik = paginator.get_page(page_number)

    return render(request, "admin_dashboard/kritik_saran.html", {"kritik": kritik})


@login_required
@user_passes_test(is_admin)
def statistik_page(request):
    tipe_kamar_list = TipeKamar.objects.all()
    return render(request, "admin_dashboard/statistik.html", {"tipe_kamar_list": tipe_kamar_list})


@login_required
@user_passes_test(is_admin)
def statistik_penghuni(request):
    tipe_kamar_id = request.GET.get("tipe_kamar")  # Retrieve filter parameter

    penghuni_query = CustomUser.objects.filter(is_penghuni=True)
    if tipe_kamar_id:
        penghuni_query = penghuni_query.filter(
            pemesanan__kamar__tipe_kamar_id=tipe_kamar_id
        )

    total_penghuni_aktif = penghuni_query.count()

    bulan_ini = now().month
    tahun_ini = now().year

    total_penghuni_baru = penghuni_query.filter(
        tanggal_bergabung__month=bulan_ini, tanggal_bergabung__year=tahun_ini
    ).count()

    total_penghuni_keluar = CustomUser.objects.filter(
        tanggal_keluar__isnull=False,  # ✅ Only count users who have exited
        tanggal_keluar__month=bulan_ini,
        tanggal_keluar__year=tahun_ini
    ).count()

    # ✅ Debugging print (Check if users have the correct exit date)
    print("📊 Users who exited this month:", CustomUser.objects.filter(
        tanggal_keluar__month=bulan_ini, tanggal_keluar__year=tahun_ini
    ).values("username", "tanggal_keluar"))

    # ✅ Continue with the rest of your logic
    total_kamar = TipeKamar.objects.aggregate(total=Sum("jumlah_kamar"))["total"] or 0
    kamar_terisi = Kamar.objects.filter(penghuni_sekarang__gt=0).count()
    kamar_kosong = max(0, total_kamar - kamar_terisi)

    lunas = Transaksi.objects.filter(status=StatusPembayaran.LUNAS).count()
    belum_lunas = Transaksi.objects.filter(status=StatusPembayaran.BELUM_LUNAS).count()

    metode_transfer = Transaksi.objects.filter(metode_pembayaran="bank_transfer").count()
    metode_ewallet = Transaksi.objects.filter(metode_pembayaran="e_wallet").count()

    pendapatan_bulanan = {}
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        revenue = Transaksi.objects.filter(
            tanggal_pembayaran__month=month, tanggal_pembayaran__year=tahun_ini
        ).aggregate(total=Sum("nominal"))["total"] or 0
        pendapatan_bulanan[month_name] = int(revenue)

    data = {
        "total_penghuni_aktif": total_penghuni_aktif,
        "total_penghuni_baru": total_penghuni_baru,
        "total_penghuni_keluar": total_penghuni_keluar,
        "pemesanan_kamar": {"terisi": kamar_terisi, "kosong": kamar_kosong},
        "pembayaran": {"lunas": lunas, "belum_lunas": belum_lunas},
        "metode_pembayaran": {"bank_transfer": metode_transfer, "e_wallet": metode_ewallet},
        "pendapatan": pendapatan_bulanan,
    }

    return JsonResponse(data)
