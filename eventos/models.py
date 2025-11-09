from django.db import models
from usuarios.models import Usuario

from django.conf import settings


class Evento(models.Model):
    TIPO_EVENTO = [
        ('cine', 'Cine / Teatro (Butacas Numeradas)'),
        ('fiesta', 'Fiesta / Concierto (Sectores / Mesas)')
    ]
    ESTADO_EVENTO = [
        ('pendiente', 'Pendiente'),
        ('publicado', 'Publicado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO, default='fiesta')
    estado = models.CharField(max_length=20, choices=ESTADO_EVENTO, default='pendiente')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    precio = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre



class Funcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.evento.nombre} - {self.fecha} {self.hora}"


# ✅ Para eventos estilo TEATRO/CONCIERTO (zonas sin asiento fijo)
class Sector(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)  # Ej: PLATEA, CANCHA VIP
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.funcion.evento.nombre}"


# ✅ Para eventos estilo CINE (asientos numerados)
class Sala(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.funcion}"


class Butaca(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)
    fila = models.CharField(max_length=1, null=True, blank=True)
    numero = models.PositiveIntegerField(null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fila}{self.numero}" if self.fila and self.numero else "Butaca sin numerar"


class Ticket(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL)
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)

    # 🔥 IMPORTANTE → Solo uno será usado según el tipo de evento
    sector = models.ForeignKey(Sector, null=True, blank=True, on_delete=models.SET_NULL)
    butaca = models.ForeignKey(Butaca, null=True, blank=True, on_delete=models.SET_NULL)

    precio = models.DecimalField(max_digits=8, decimal_places=2)
    pagado = models.BooleanField(default=False)
    invitado_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        modo = "Butaca" if self.butaca else "Sector"
        return f"Ticket {self.id} - {modo}"
