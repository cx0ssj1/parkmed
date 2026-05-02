from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class RegistroEstacionamiento(models.Model):
    ESTADO_PROGRAMADO = "PROGRAMADO"
    ESTADO_EN_PROCESO = "EN_PROCESO"
    ESTADO_EN_URGENCIA = "EN_URGENCIA"
    ESTADO_FINALIZADO = "FINALIZADO"

    ESTADOS = [
        (ESTADO_PROGRAMADO, "Programado"),
        (ESTADO_EN_PROCESO, "En proceso"),
        (ESTADO_EN_URGENCIA, "En urgencia"),
        (ESTADO_FINALIZADO, "Finalizado"),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="estacionamientos")
    rut_paciente = models.CharField(max_length=10)
    nombre_paciente = models.CharField(max_length=150)
    patente = models.CharField(max_length=6)
    
    fecha_hora_medica = models.DateTimeField(null=True, blank=True)
    foto_hora_medica = models.ImageField(upload_to="horas_medicas/", null=True, blank=True)
    movilidad_reducida = models.BooleanField(default=False)
    es_urgencia = models.BooleanField(default=False)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PROGRAMADO)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-creado_en']
        verbose_name = "Registro de Estacionamiento"
        verbose_name_plural = "Registros de Estacionamiento"
    def __str__(self):
        return f"{self.patente} - {self.nombre_paciente} ({self.estado})"
    
    @property
    def duracion_horas(self):
        return 5 if self.movilidad_reducida else 3
    @property
    def margen_minutos(self):
        return 60 if self.movilidad_reducida else 30
    @property
    def hora_inicio_proteccion(self):
        if self.es_urgencia:
            return self.creado_en
        if self.fecha_hora_medica:
            return self.fecha_hora_medica - timedelta(minutes=self.margen_minutos)
        return None

    @property
    def hora_fin_proteccion(self):
        if self.es_urgencia:
            base = self.creado_en
        elif self.fecha_hora_medica:
            base = self.fecha_hora_medica
        else:
            return None
        return base + timedelta(
            hours=self.duracion_horas,
            minutes=self.margen_minutos
        )