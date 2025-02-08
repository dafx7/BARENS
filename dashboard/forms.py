from django import forms
from .models import Transaksi


class UploadBuktiForm(forms.ModelForm):
    JENIS_DURASI_CHOICES = [
        ("per_bulan", "Per Bulan"),
        ("per_tahun", "Per Tahun")
    ]

    jenis_durasi = forms.ChoiceField(
        choices=JENIS_DURASI_CHOICES,
        label="Jenis Pembayaran",
        widget=forms.Select(attrs={"class": "w-full border-gray-300 rounded-lg focus:ring-[#A3B18A]"})
    )

    durasi_bayar = forms.ChoiceField(
        choices=[(i, f"{i} Bulan") for i in range(1, 13)],  # 1-12 months
        label="Durasi Pembayaran",
        widget=forms.Select(attrs={"class": "w-full border-gray-300 rounded-lg focus:ring-[#A3B18A]"})
    )

    class Meta:
        model = Transaksi
        fields = ["tanggal_pembayaran", "nominal", "metode_pembayaran", "bukti_transfer", "jenis_durasi", "durasi_bayar"]
