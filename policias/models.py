from django.db import models
from django.contrib.auth.models import User


class Policia(models.Model):
    INSTITUCION_CARABINEROS = "CARABINEROS"
    INSTITUCION_MUNICIPAL = "MUNICIPAL"

    INSTITUCIONES = [
        (INSTITUCION_CARABINEROS, "Carabineros"),
        (INSTITUCION_MUNICIPAL, "Policía Municipal"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="policia"
    )
    rut = models.CharField(max_length=12, unique=True)
    institucion = models.CharField(
        max_length=15,
        choices=INSTITUCIONES,
        default=INSTITUCION_CARABINEROS
    )
    numero_placa = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Solo si pertenece a Carabineros."
    )

    def __str__(self):
        nombre = self.user.get_full_name() or self.user.username
        return f"{nombre} ({self.get_institucion_display()})"

    @property
    def es_carabinero(self):
        return self.institucion == self.INSTITUCION_CARABINEROS