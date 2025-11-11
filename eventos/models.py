from django.db import models
from usuarios.models import Usuario

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, blank=True)
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='ubicaciones/', blank=True, null=True)

    def capacidad(self):
        return self.filas * self.columnas

    def __str__(self):
        return self.nombre
    
class Evento(models.Model):
    ESTADO_EVENTO = [
        ('pendiente', 'Pendiente'),
        ('publicado', 'Publicado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, related_name='eventos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_EVENTO, default='pendiente')
    precio_ticket = models.IntegerField(default=0)

    def __str__(self):
            return self.nombre
    
    def clean(self):
        from django.core.exceptions import ValidationError
        eventos_conflicto = Evento.objects.filter(
            ubicacion=self.ubicacion,
            fecha=self.fecha,
            hora=self.hora
        ).exclude(pk=self.pk)
        if eventos_conflicto.exists():
            raise ValidationError("Ya hay un evento en esta ubicación a esta fecha y hora.")


    
class AsientoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='asientos')
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('evento', 'fila', 'columna')

    def __str__(self):
        return f"Fila {self.fila} - Col {self.columna} - {'Libre' if self.disponible else 'Ocupado'}"