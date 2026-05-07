from django import forms
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