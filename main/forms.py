from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

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
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full mt-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#A3B18A]",
            "placeholder": "Masukan email"
        })
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
        fields = ["username", "first_name", "email", "phone_number", "password1", "password2"]


from .models import Pemesanan, TipeKamar

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
                self.fields['jumlah_penghuni'].choices = [(i, f"{i} orang") for i in range(1, tipe_kamar.max_penghuni + 1)]
            except (ValueError, TypeError, TipeKamar.DoesNotExist):
                pass

