from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente')
    rut = models.CharField(max_length=10, unique=True)
    celular = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut})"