from django.urls import path
from .views import *



urlpatterns = [
    path('acerca/', acerca, name='acerca'),
    path('', home, name='home'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('login/', iniciar_sesion, name='iniciar_sesion'),
    path('logout/', cerrar_sesion, name='logout'),
]
