from django.contrib import admin
from .models import Evento, Funcion, Sala, Butaca, Ticket, Sector

# Register your models here.
admin.site.register(Evento)
admin.site.register(Funcion)    
admin.site.register(Sala)
admin.site.register(Butaca)
admin.site.register(Ticket)
admin.site.register(Sector)