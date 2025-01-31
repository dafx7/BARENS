from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TipeKamar, KamarImage, Pemesanan, CustomUser


class CustomUser(AbstractUser):  # Inherit Django's User model
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


admin.site.register(TipeKamar)
admin.site.register(KamarImage)
admin.site.register(Pemesanan)
admin.site.register(CustomUser)
