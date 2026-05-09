from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Paciente
from policias.models import Policia


class PacienteInline(admin.StackedInline):
    model = Paciente
    can_delete = False
    verbose_name_plural = "Perfil de paciente"
    fk_name = "user"


class PoliciaInline(admin.StackedInline):
    model = Policia
    can_delete = False
    verbose_name_plural = "Perfil de policía"
    fk_name = "user"


class UsuarioAdmin(UserAdmin):
    inlines = [PacienteInline, PoliciaInline]
    list_display = [
        "username",
        "first_name",
        "email",
        "rol",
        "is_active",
        "is_staff",
    ]
    list_filter = ["is_staff", "is_active"]

    def rol(self, obj):
        if hasattr(obj, "policia"):
            return f"{obj.policia.get_institucion_display()}"
        if hasattr(obj, "paciente"):
            return "Paciente"
        if obj.is_superuser:
            return "Administrador"
        return "—"
    rol.short_description = "Rol"

admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ["user", "rut", "celular"]
    search_fields = ["rut", "user__first_name", "user__email"]