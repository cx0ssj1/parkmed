from django import forms
from django.contrib.auth.models import User
from .models import Paciente

class RegistroPacienteForm(forms.Form):
    nombre_completo = forms.CharField(
        label="Nombre completo",
        max_length=150
    )
    rut = forms.CharField(
        label="RUT",
        max_length=10,
        help_text="Ej: 12345678-9"
    )
    email = forms.EmailField(label="Email de contacto")
    celular = forms.CharField(
        label="Número de celular",
        max_length=9,
        help_text="Ej: 912345678"
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=6
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput
    )

    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        if Paciente.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Ya existe un usuario con este RUT.")
        return rut

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        password_confirm = cleaned.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned
class LoginPacienteForm(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)