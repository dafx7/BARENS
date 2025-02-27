from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, Kamar, KamarImage, Pemesanan, CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = list(UserAdmin.fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni')})
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        (None, {'fields': ('phone_number', 'is_penghuni')})
    ]

    list_display = ['username', 'phone_number', 'is_penghuni', 'is_staff', 'is_active']  # Hapus email
    search_fields = ['username', 'phone_number']  # Hapus email
    list_filter = ['is_penghuni', 'is_staff', 'is_active']


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
