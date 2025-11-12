from django.db import models
from usuarios.models import Usuario
from eventos.models import AsientoEvento

class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    asientos_nombres = models.CharField(max_length=255, null=True, blank=True)
    evento_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"
    
class Pago(models.Model):
    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE, null=True, blank=True)
    metodo = models.CharField(max_length=50, default='Simulado')
    estado = models.CharField(max_length=20, choices=ESTADO_PAGO, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - {self.estado}"



class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    asiento = models.ForeignKey(AsientoEvento, on_delete=models.PROTECT)  # cada ticket un asiento
    nombre_asiento = models.CharField(max_length=10, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcular subtotal y nombre del asiento
        self.subtotal = self.asiento.evento.precio_ticket
        self.nombre_asiento = self.asiento.nombre
        
        # Marcar asiento como ocupado
        self.asiento.disponible = False
        self.asiento.save()

        super().save(*args, **kwargs)

        # ✅ Actualizar la compra con los asientos y el evento
        asientos = self.compra.detalles.values_list('nombre_asiento', flat=True)
        self.compra.asientos_nombres = ', '.join(asientos)
        self.compra.evento_id = self.asiento.evento.id
        self.compra.save()
