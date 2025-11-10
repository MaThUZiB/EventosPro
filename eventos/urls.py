from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('buscar/', views.buscar_eventos, name='buscar_eventos'),
    path('buscar_eventos_ajax/', views.buscar_eventos_ajax, name='buscar_eventos_ajax'),
    path('', views.listar_eventos, name='listar_eventos'),
    path('detalle/<int:id>/', views.detalle_evento, name='detalle_evento'),
    path('mis_eventos/', views.mis_eventos, name='mis_eventos'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('editar/<int:id>/', views.editar_evento, name='editar_evento'),
    path('eliminar/<int:id>/', views.eliminar_evento, name='eliminar_evento'),
    path('tickets/', views.listar_tickets, name='listar_tickets'),
    path('funcion/<int:funcion_id>/butacas/', views.seleccionar_butacas, name='seleccionar_butacas'),
    path('checkout/', views.checkout, name='checkout'),
    path('comprar-invitado/', views.comprar_invitado, name='comprar_invitado'),
]
