from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, Kamar, KamarImage, Pemesanan, CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Extend the default UserAdmin fieldsets to include phone_number and is_penghuni
    fieldsets = list(UserAdmin.fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni')})  # Add is_penghuni
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni')})  # Add is_penghuni to add form
    ]

    list_display = ['username', 'email', 'phone_number', 'is_penghuni', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['is_penghuni', 'is_staff', 'is_active']  # Add filtering by is_penghuni


# ✅ Kamar Admin Panel
class KamarAdmin(admin.ModelAdmin):
    list_display = ['nomor_kamar', 'tipe_kamar', 'kapasitas', 'penghuni_sekarang', 'is_full']
    list_filter = ['tipe_kamar', 'kapasitas']
    search_fields = ['nomor_kamar']

# ✅ Pemesanan Admin Panel
class PemesananAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kontak', 'kamar', 'status', 'tanggal_mulai', 'durasi']
    list_filter = ['status']
    search_fields = ['nama', 'kontak']


# Register models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TipeKamar)
admin.site.register(Kamar, KamarAdmin)  # ✅ Added
admin.site.register(KamarImage)
admin.site.register(Pemesanan, PemesananAdmin)  # ✅ Added Admin Panel for Pemesanan
