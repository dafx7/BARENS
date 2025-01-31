from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "Masukan nomor handphone yang aktif"}),
        required=True
    )

    class Meta:
        model = CustomUser  # Pakai CustomUser bukan User
        fields = ["first_name", "email", "phone_number", "password1", "password2"]
