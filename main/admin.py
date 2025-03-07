from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, Kamar, KamarImage, Pemesanan, CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = list(UserAdmin.fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni', 'tanggal_bergabung', 'tanggal_keluar')})
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni', 'tanggal_bergabung', 'tanggal_keluar')})
    ]

    list_display = ['username', 'phone_number', 'is_penghuni', 'is_staff', 'is_active']
    search_fields = ['username', 'phone_number']
    list_filter = ['is_penghuni', 'is_staff', 'is_active']


# ✅ Kamar Admin Panel
class KamarAdmin(admin.ModelAdmin):
    list_display = ['nomor_kamar', 'lantai', 'kapasitas', 'penghuni_sekarang', 'is_full']  # ✅ Hapus tipe_kamar
    list_filter = ['lantai', 'kapasitas']  # ✅ Ganti tipe_kamar dengan lantai
    search_fields = ['nomor_kamar']


# ✅ Pemesanan Admin Panel
class PemesananAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kontak', 'tipe_kamar', 'status', 'tanggal_mulai', 'durasi']
    list_filter = ['status', 'tipe_kamar']
    search_fields = ['nama', 'kontak']


# Register models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TipeKamar)
admin.site.register(Kamar, KamarAdmin)  # ✅ Fixed
admin.site.register(KamarImage)
admin.site.register(Pemesanan, PemesananAdmin)  # ✅ Fixed
