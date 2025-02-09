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
    Menampilkan daftar penghuni dengan pagination.
    """
    penghuni_list = CustomUser.objects.all().order_by('-id')  # Menampilkan pengguna terbaru dulu
    paginator = Paginator(penghuni_list, 5)  # 5 penghuni per halaman
    page_number = request.GET.get("page")
    penghuni = paginator.get_page(page_number)

    return render(request, "admin_dashboard/pengelolaan_akun.html", {"penghuni": penghuni})


@login_required
@user_passes_test(is_admin)
def tambah_penghuni(request):
    if request.method == "POST":
        nama = (request.POST.get("nama") or "").strip()
        email = (request.POST.get("email") or "").strip()
        phone_number = (request.POST.get("phone_number") or "").strip()
        is_penghuni = request.POST.get("is_penghuni") == "on"  # Checkbox handling

        # Cek apakah field kosong
        if not nama or not email or not phone_number:
            messages.error(request, "Semua field wajib diisi!")
            return redirect("kelola_penghuni")

        # Validasi apakah email sudah digunakan
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan!")
            return redirect("kelola_penghuni")

        # Buat akun penghuni baru
        user = CustomUser.objects.create(
            username=email.split("@")[0],
            email=email,
            phone_number=phone_number,
            is_penghuni=is_penghuni  # Tambahkan status penghuni
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
        user.username = request.POST.get("nama").strip()
        user.email = request.POST.get("email").strip()
        user.phone_number = request.POST.get("phone_number").strip()
        user.is_penghuni = True if request.POST.get("is_penghuni") == "on" else False  # Simpan nilai checkbox

        user.save()
        messages.success(request, "Data penghuni berhasil diperbarui!")
        return redirect("kelola_penghuni")

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
