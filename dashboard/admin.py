from django.contrib import admin
from .models import Pembayaran


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ("user", "tanggal_pembayaran", "jumlah_pembayaran", "status", "jatuh_tempo_berikutnya")
    search_fields = ("user__username", "status")

