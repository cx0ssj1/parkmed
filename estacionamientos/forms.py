from django import forms

from core.validators import normalizar_rut, validar_rut
from .models import RegistroEstacionamiento
from django.utils.timezone import make_aware, is_naive

class RegistroEstacionamientoForm(forms.ModelForm):
    class Meta:
        model = RegistroEstacionamiento
        fields = [
            "rut_paciente",
            "nombre_paciente",
            "patente",
            "fecha_hora_medica",
            "foto_hora_medica",
            "movilidad_reducida",
            "es_urgencia"
        ]
        widgets = {
            "fecha_hora_medica": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }
        labels = {
            "rut_paciente": "RUT del paciente",
            "nombre_paciente": "Nombre del paciente",
            "patente": "Patente del vehículo",
            "fecha_hora_medica": "Fecha y hora de la atención médica",
            "foto_hora_medica": "Foto de la hora médica (opcional)",
            "movilidad_reducida": "El paciente tiene movilidad reducida o es adulto mayor",
            "es_urgencia": "Es atención de urgencia (sin hora previa)",
        }
        help_texts = {
            "patente": "Sin guion, ej: ABCD12",
            "movilidad_reducida": "Activa esto si vas a adjuntar carnet de discapacidad o adulto mayor.",
            "es_urgencia": "Si activas esto, la fecha y hora de la atención no es necesaria.",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rut_paciente"].widget.attrs.update({
            "pattern": r"[0-9\.]+-?[0-9kK]",
            "title": "Ingresa un RUT válido, ej: 12345678-9",
            "placeholder": "12345678-9",
        })
    def clean_rut_paciente(self):
        rut = self.cleaned_data["rut_paciente"]
        validar_rut(rut)
        return normalizar_rut(rut)
    def clean(self):
        cleaned = super().clean()
        es_urgencia = cleaned.get("es_urgencia")
        fecha = cleaned.get("fecha_hora_medica")
        if not es_urgencia and not fecha:
            raise forms.ValidationError(
                "Debes indicar la fecha y hora de la atención médica, "
                "o marcar que es una atención de urgencia."
            )
        if fecha and is_naive(fecha):
            cleaned["fecha_hora_medica"] = make_aware(fecha)
        return cleaned
class EditarRegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroEstacionamiento
        fields = [
            "fecha_hora_medica",
            "foto_hora_medica",
            "movilidad_reducida",
        ]
        widgets = {
            "fecha_hora_medica": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        labels = {
            "fecha_hora_medica": "Fecha y hora de la atención médica",
            "foto_hora_medica": "Foto de la hora médica",
            "movilidad_reducida": "El paciente tiene movilidad reducida o es adulto mayor",
        }
        help_texts = {
            "foto_hora_medica": "Puedes subir o reemplazar el comprobante de tu atención.",
        }

    def clean(self):
        cleaned = super().clean()
        es_urgencia = self.instance.es_urgencia
        fecha = cleaned.get("fecha_hora_medica")

        if not es_urgencia and not fecha:
            raise forms.ValidationError(
                "Debes indicar la fecha y hora de la atención médica."
            )

        if fecha and is_naive(fecha):
            cleaned["fecha_hora_medica"] = make_aware(fecha)

        return cleaned