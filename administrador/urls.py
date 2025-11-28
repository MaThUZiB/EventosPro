from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('', views.admin_inicio, name='admin_inicio'),
    path("usuarios/", views.listar_usuarios_admin, name="listar_usuarios_admin"),
    path("usuarios/<int:user_id>/editar/", views.editar_usuario_admin, name="editar_usuario_admin"),
    path("usuarios/<int:user_id>/eliminar/", views.eliminar_usuario_admin, name="eliminar_usuario_admin"),
    path("eventos/", views.listar_eventos_admin, name="listar_eventos_admin"),
    path("eventos/<int:id>/editar/", views.editar_evento_admin, name="editar_evento_admin"),
    path("eventos/<int:id>/eliminar/", views.eliminar_evento_admin, name="eliminar_evento_admin"),
    path('compras/', views.listar_compras_admin, name='listar_compras_admin'),
    path('compras/<int:compra_id>/', views.ver_compra_admin, name='ver_compra_admin'),
    path('compras/<int:compra_id>/eliminar/', views.eliminar_compra_admin, name='eliminar_compra_admin'),
    path('ubicaciones/', views.listar_ubicaciones_admin, name='listar_ubicaciones_admin'),
    path('ubicaciones/crear/', views.crear_ubicacion_admin, name='crear_ubicacion_admin'),
    path('ubicaciones/editar/<int:id>/', views.editar_ubicacion_admin, name='editar_ubicacion_admin'),
    path('ubicaciones/eliminar/<int:id>/', views.eliminar_ubicacion_admin, name='eliminar_ubicacion_admin'),
]
