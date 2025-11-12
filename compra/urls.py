from django.urls import path
from . import views
from .views import *

app_name = 'compra'

urlpatterns = [
    path("confirmar_compra/<int:compra_id>/", views.confirmar_compra, name="confirmar_compra"),
    path("procesar_pago/<int:compra_id>/", views.procesar_pago, name="procesar_pago"),
    path("confirmacion/<int:compra_id>/", views.confirmacion_compra, name="confirmacion_compra"),
]
