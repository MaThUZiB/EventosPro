from django.urls import path
from .views import *


urlpatterns = [
    path('detalle/<int:id>/', detalle_evento, name='detalle_evento'),
    path('mis_eventos/', mis_eventos, name='mis_eventos'),
    path('crear/', crear_evento, name='crear_evento'),
    path('editar/<int:id>/', editar_evento, name='editar_evento'),
    path('eliminar/<int:id>/', eliminar_evento, name='eliminar_evento'),
]