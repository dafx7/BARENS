from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, KamarImage, Pemesanan, CustomUser


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


# Register models in Django Admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TipeKamar)
admin.site.register(KamarImage)
admin.site.register(Pemesanan)
