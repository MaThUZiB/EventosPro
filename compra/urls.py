from django.urls import path
from . import views
from .views import *

app_name = 'compra'

urlpatterns = [
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('detalle/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
    path('descargar-entrada/<int:compra_id>/', views.descargar_entrada, name='descargar_entrada'),
    path("confirmar_compra/<int:compra_id>/", views.confirmar_compra, name="confirmar_compra"),
    path("procesar_pago/<int:compra_id>/", views.procesar_pago, name="procesar_pago"),
    path("confirmacion/<int:compra_id>/", views.confirmacion_compra, name="confirmacion_compra"),
]
