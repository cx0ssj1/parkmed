from django.contrib import admin
from .models import RegistroEstacionamiento

@admin.register(RegistroEstacionamiento)
class RegistroEstacionamientoAdmin(admin.ModelAdmin):
    list_display = ["patente", "nombre_paciente", "estado", "creado_en"]
    list_filter = ["estado", "es_urgencia", "movilidad_reducida"]
    search_fields = ["patente", "rut_paciente", "nombre_paciente"]