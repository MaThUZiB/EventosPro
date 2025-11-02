from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    tipo_usuario = models.CharField(max_length=50, blank=True, choices=[
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
        ('organizador', 'Organizador'),
    ])

    USERNAME_FIELD = 'username'  # indica que se usa 'username' para login
    REQUIRED_FIELDS = ['email', 'rut']  # campos obligatorios para createsuperuser
    
    def __str__(self):
        return self.username