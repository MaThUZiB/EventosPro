from django.contrib import admin
from .models import Evento, AsientoEvento, Ubicacion

# Register your models here.
admin.site.register(Evento)
admin.site.register(AsientoEvento)
admin.site.register(Ubicacion)