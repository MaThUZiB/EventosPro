from django.db import models
from usuarios.models import Usuario

class Evento(models.Model):
    ESTADO_EVENTO = [
        ('pendiente', 'Pendiente'),
        ('publicado', 'Publicado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=20, blank=True)

    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_EVENTO, default='pendiente')
    
    precio_ticket = models.IntegerField(default=0)
    stock_ticket = models.IntegerField(default=0)
    capacidad = models.PositiveIntegerField(default=100)

    def save(self, *args, **kwargs):
        nuevo = self.pk is None
        super().save(*args, **kwargs)
        if nuevo:
            crear_asientos_eventos(self)

    def __str__(self):
        return self.nombre
    
class Asiento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="asientos")
    fila = models.CharField(max_length=5)
    numero = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('evento', 'fila', 'numero')

    def __str__(self):
        return f"{self.fila}{self.numero} - {'Libre' if self.disponible else 'Ocupado'}"

def crear_asientos_eventos(evento):
    import string
    filas = list(string.ascii_uppercase[:evento.capacidad // 10])
    numero = 1
    for fila in filas:
        for n in range(1,11):
            if numero > evento.capacidad:
                return 
            Asiento.objects.create(evento=evento, fila=fila, numero =n)
            numero +=1
