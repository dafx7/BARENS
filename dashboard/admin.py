from django.contrib import admin
from .models import Pembayaran, Transaksi

@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ('user', 'tanggal_pembayaran', 'jumlah_pembayaran', 'status', 'jatuh_tempo_berikutnya')
    list_filter = ('status', 'tanggal_pembayaran')
    search_fields = ('user__username', 'jumlah_pembayaran')

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('user', 'bulan', 'nominal', 'metode_pembayaran', 'status', 'tanggal_transaksi')
    list_filter = ('status', 'metode_pembayaran')
    search_fields = ('user__username', 'bulan')
