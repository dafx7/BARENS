from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from main.models import CustomUser, Pemesanan

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

    # Jika ada pencarian, filter berdasarkan nama lengkap atau email
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
        "query": query,  # Kirim kembali query ke template
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
            is_penghuni=is_penghuni
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

    if request.method == "POST":
        user.username = (request.POST.get("nama") or "").strip()
        user.email = (request.POST.get("email") or "").strip()
        user.phone_number = (request.POST.get("phone_number") or "").strip()
        user.is_penghuni = request.POST.get("is_penghuni") == "on"  # Handle checkbox safely

        if not user.username or not user.email or not user.phone_number:
            messages.error(request, "All fields are required!")
            return redirect("edit_penghuni", user_id=user.id)

        user.save()

        # Success Message
        messages.success(request, "Data penghuni berhasil diperbarui!")

        return redirect("kelola_penghuni")  # Redirect back to the list

    return render(request, "admin_dashboard/edit_penghuni.html", {"user": user})


@login_required
@user_passes_test(is_admin)
def hapus_penghuni(request, user_id):
    """
    Menghapus akun penghuni.
    """
    user = get_object_or_404(CustomUser, id=user_id)
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
