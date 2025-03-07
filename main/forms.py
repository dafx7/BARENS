from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Pemesanan, Kamar

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Masukan username"
        }),
        required=True
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Masukan nama lengkap"
        }),
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Masukan nomor handphone yang aktif"
        }),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Minimal 8 karakter"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Masukan kembali password"
        })
    )

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "phone_number", "password1", "password2"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Nomor handphone sudah digunakan. Gunakan nomor lain.")
        return phone_number


class PemesananForm(forms.ModelForm):
    tipe_sewa = forms.ChoiceField(
        label="Tipe Sewa",
        choices=[('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    durasi = forms.IntegerField(
        label="Durasi",
        min_value=1,
        required=True,
        help_text="Masukkan jumlah bulan atau tahun sesuai tipe sewa",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    jumlah_penghuni = forms.ChoiceField(
        label="Jumlah Penghuni",
        choices=[(1, "1 Orang"), (2, "2 Orang"), (3, "3 Orang")],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Pemesanan
        fields = ['nama', 'kontak', 'tipe_kamar', 'tipe_sewa', 'durasi', 'jumlah_penghuni', 'tanggal_mulai']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tipe_kamar' in self.data:
            try:
                tipe_kamar = TipeKamar.objects.get(id=int(self.data.get('tipe_kamar')))
                max_penghuni = tipe_kamar.max_penghuni
                self.fields['jumlah_penghuni'].choices = [(i, f"{i} Orang") for i in range(1, max_penghuni + 1)]
            except (ValueError, TypeError, TipeKamar.DoesNotExist):
                pass
