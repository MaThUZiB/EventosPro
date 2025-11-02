from django.db import models
from usuarios.models import Usuario 

# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre