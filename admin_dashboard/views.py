from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from main.models import CustomUser

def is_admin(user):
    return user.is_staff  # Only allow staff/admin users


@login_required
@user_passes_test(is_admin)
def kelola_penghuni(request):
    penghuni = CustomUser.objects.all()
    return render(request, "admin_dashboard/pengelolaan_akun.html", {"penghuni": penghuni})


@login_required
@user_passes_test(is_admin)
def toggle_status_penghuni(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"Akun {user.username} {'diaktifkan' if user.is_active else 'dinonaktifkan'}.")
    return redirect("kelola_penghuni")
