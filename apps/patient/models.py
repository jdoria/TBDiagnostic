from django.db import models
from datetime import date


# Create your models here.

class Patient(models.Model):
    codigo = models.CharField(max_length=15)
    edad = models.IntegerField()
    sexo = models.NullBooleanField(default=None)
    vih = models.NullBooleanField(default=None)
    diabetes = models.NullBooleanField(default=None)
    hab_calle = models.NullBooleanField(default=None)
    info_clinica = models.NullBooleanField(default=None)
    observaciones = models.TextField()
    fecha_creacion = models.DateField(default=date.today)
    validacion = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.codigo)
