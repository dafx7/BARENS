from django.contrib import admin
from .models import Pembayaran, Transaksi, KritikSaran


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ("user", "jatuh_tempo")  # ✅ Only keep existing fields
    search_fields = ("user__username",)  # ✅ Allow searching by user
    ordering = ("jatuh_tempo",)  # ✅ Sort by due date

admin.site.register(Transaksi)


admin.site.register(KritikSaran)
