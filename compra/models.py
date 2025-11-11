from django.db import models
from usuarios.models import Usuario
from eventos.models import Evento, Asiento

# Create your models here.
class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"
    

class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.PROTECT)  # cada ticket un asiento
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.evento.precio_ticket
        super().save(*args, **kwargs)
        # Marcar el asiento como ocupado
        self.asiento.disponible = False
        self.asiento.save()

class Pago(models.Model):
    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50, default='Simulado')
    estado = models.CharField(max_length=20, choices=ESTADO_PAGO, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - {self.estado}"