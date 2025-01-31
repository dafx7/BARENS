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
