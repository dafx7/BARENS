from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, KamarImage, Pemesanan, CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = list(UserAdmin.fieldsets) + [  # Salin fieldsets dari UserAdmin
        (None, {'fields': ('phone_number',)})  # Tambahkan hanya phone_number
    ]

    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        (None, {'fields': ('phone_number',)})  # Tambahkan hanya phone_number
    ]

    list_display = ['username', 'email', 'phone_number', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone_number']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TipeKamar)
admin.site.register(KamarImage)
admin.site.register(Pemesanan)
