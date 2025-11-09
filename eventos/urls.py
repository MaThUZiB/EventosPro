from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.listar_eventos, name='listar_eventos'),

    path('detalle/<int:id>/', views.detalle_evento, name='detalle_evento'),
    path('mis_eventos/', views.mis_eventos, name='mis_eventos'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('editar/<int:id>/', views.editar_evento, name='editar_evento'),
    path('eliminar/<int:id>/', views.eliminar_evento, name='eliminar_evento'),

    path('funcion/<int:funcion_id>/butacas/', views.seleccionar_butacas, name='seleccionar_butacas'),
    path('checkout/', views.checkout, name='checkout'),
    path('comprar-invitado/', views.comprar_invitado, name='comprar_invitado'),
]
