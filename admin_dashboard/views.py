from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from main.models import CustomUser

# Fungsi untuk membatasi akses hanya untuk admin
def is_admin(user):
    return user.is_staff  # Hanya admin yang bisa mengakses


@login_required
@user_passes_test(is_admin)
def kelola_penghuni(request):
    """
    Menampilkan daftar penghuni dengan pagination (5 per halaman).
    """
    penghuni_list = CustomUser.objects.all().order_by('-id')  # Menampilkan pengguna terbaru dulu
    paginator = Paginator(penghuni_list, 5)  # 5 penghuni per halaman
    page_number = request.GET.get("page")
    penghuni = paginator.get_page(page_number)

    return render(request, "admin_dashboard/pengelolaan_akun.html", {
        "penghuni": penghuni,
        "paginator": paginator,  # Tambahkan objek paginator untuk navigasi
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
