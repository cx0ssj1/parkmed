from django import forms
from django.contrib.auth.models import User
from core.validators import validar_rut, normalizar_rut


class CrearUsuarioForm(forms.Form):
    ROL_PACIENTE = "PACIENTE"
    ROL_POLICIA = "POLICIA"
    ROLES = [
        (ROL_PACIENTE, "Paciente"),
        (ROL_POLICIA, "Policía"),
    ]

    INSTITUCION_CARABINEROS = "CARABINEROS"
    INSTITUCION_MUNICIPAL = "MUNICIPAL"
    INSTITUCIONES = [
        (INSTITUCION_CARABINEROS, "Carabineros"),
        (INSTITUCION_MUNICIPAL, "Policía Municipal"),
    ]

    rol = forms.ChoiceField(label="Tipo de usuario", choices=ROLES)
    nombre_completo = forms.CharField(label="Nombre completo", max_length=150)
    rut = forms.CharField(label="RUT", max_length=12, help_text="Ej: 12345678-9")
    email = forms.EmailField(label="Email", required=False)
    celular = forms.CharField(
        label="Celular",
        max_length=15,
        required=False,
        help_text="Solo para pacientes."
    )
    institucion = forms.ChoiceField(
        label="Institución",
        choices=INSTITUCIONES,
        required=False,
        help_text="Solo para policías."
    )
    numero_placa = forms.CharField(
        label="Número de placa",
        max_length=10,
        required=False,
        help_text="Solo para Carabineros."
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        min_length=6
    )

    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        validar_rut(rut)
        rut = normalizar_rut(rut)
        if User.objects.filter(username=rut).exists():
            raise forms.ValidationError("Ya existe un usuario con este RUT.")
        return rut

    def clean(self):
        cleaned = super().clean()
        rol = cleaned.get("rol")

        if rol == self.ROL_PACIENTE and not cleaned.get("celular"):
            self.add_error("celular", "El celular es obligatorio para pacientes.")

        if rol == self.ROL_POLICIA and not cleaned.get("institucion"):
            self.add_error("institucion", "La institución es obligatoria para policías.")

        return cleaned
class EditarUsuarioForm(forms.Form):

    INSTITUCION_CARABINEROS = "CARABINEROS"
    INSTITUCION_MUNICIPAL = "MUNICIPAL"
    INSTITUCIONES = [
        (INSTITUCION_CARABINEROS, "Carabineros"),
        (INSTITUCION_MUNICIPAL, "Policía Municipal"),
    ]

    nombre_completo = forms.CharField(label="Nombre completo", max_length=150)
    email = forms.EmailField(label="Email", required=False)

    celular = forms.CharField(
        label="Celular",
        max_length=15,
        required=False,
        help_text="Solo para pacientes."
    )
    institucion = forms.ChoiceField(
        label="Institución",
        choices=INSTITUCIONES,
        required=False,
        help_text="Solo para policías."
    )
    numero_placa = forms.CharField(
        label="Número de placa",
        max_length=10,
        required=False,
        help_text="Solo para Carabineros."
    )

    password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False,
        min_length=6,
        help_text="Déjala en blanco para mantener la contraseña actual."
    )