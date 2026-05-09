from django.contrib import admin
from .models import Policia


@admin.register(Policia)
class PoliciaAdmin(admin.ModelAdmin):
    list_display = ["user", "rut", "institucion", "numero_placa"]
    list_filter = ["institucion"]
    search_fields = ["rut", "user__first_name", "numero_placa"]