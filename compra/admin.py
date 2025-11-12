from django.contrib import admin
from .models import Compra, CompraDetalle, Pago

# Register your models here.
admin.site.register(Compra)
admin.site.register(Pago)
admin.site.register(CompraDetalle)