from django.shortcuts import render , get_object_or_404, redirect
from compra.models import Compra 
from usuarios.models import Usuario
from eventos.models import Evento, Ubicacion
from .forms import UsuarioAdminForm, EventoAdminForm, UbicacionAdminForm
from django.contrib import messages

# Create your views here.
def admin_inicio(request):
    eventos_pendientes = Evento.objects.filter(estado = 'pendiente').count()
    eventos_activos = Evento.objects.filter(estado = 'publicado').count()
    usuarios_totales = Usuario.objects.count()
    entradas_vendidas = Compra.objects.count()
    return render(request, 'administrador/admin_inicio.html', {
        'eventos_pendientes': eventos_pendientes,
        'eventos_activos': eventos_activos,
        'usuarios_totales': usuarios_totales,
        'entradas_vendidas': entradas_vendidas
    })

def listar_usuarios_admin(request):
    usuarios = Usuario.objects.all().order_by("id")
    return render(request, "administrador/listar_usuarios_admin.html", {"usuarios": usuarios})

def editar_usuario_admin(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    
    if request.method == "POST":
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("administrador:listar_usuarios_admin")
    else:
        form = UsuarioAdminForm(instance=usuario)

    return render(request, "administrador/editar_usuario_admin.html", {"form": form, "usuario": usuario})

def eliminar_usuario_admin(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("administrador:listar_usuarios_admin")

    return render(request, "administrador/eliminar_usuario_admin.html", {"usuario": usuario})

def listar_eventos_admin(request):
    eventos = Evento.objects.all().order_by("-id")
    return render(request, "administrador/listar_eventos_admin.html", {"eventos": eventos})

def editar_evento_admin(request, id):
    evento = get_object_or_404(Evento, id=id)
    form = EventoAdminForm(request.POST or None, instance=evento)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("administrador:listar_eventos_admin")

    return render(request, "administrador/editar_evento_admin.html", {"form": form, "evento": evento})

def eliminar_evento_admin(request, id):
    evento = get_object_or_404(Evento, id=id)
    evento.delete()
    return redirect("administrador:listar_eventos_admin")

# Listar compras para admin
def listar_compras_admin(request):
    compras = Compra.objects.select_related('usuario').prefetch_related('detalles', 'pago').all().order_by('-fecha')
    return render(request, 'administrador/listar_compras_admin.html', {'compras': compras})

# Ver detalle de una compra
def ver_compra_admin(request, compra_id):
    compra = get_object_or_404(Compra.objects.select_related('usuario').prefetch_related('detalles', 'pago'), pk=compra_id)
    return render(request, 'administrador/ver_compra_admin.html', {'compra': compra})

# Eliminar compra
def eliminar_compra_admin(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    compra.delete()
    return redirect('administrador:listar_compras_admin')

# Listar todas las ubicaciones
def listar_ubicaciones_admin(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'administrador/listar_ubicaciones_admin.html', {'ubicaciones': ubicaciones})

# Crear nueva ubicación
def crear_ubicacion_admin(request):
    if request.method == 'POST':
        form = UbicacionAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrador:listar_ubicaciones_admin')
    else:
        form = UbicacionAdminForm()
    return render(request, 'administrador/crear_ubicacion_admin.html', {'form': form})

# Editar ubicación existente
def editar_ubicacion_admin(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    if request.method == 'POST':
        form = UbicacionAdminForm(request.POST, request.FILES, instance=ubicacion)
        if form.is_valid():
            form.save()
            return redirect('administrador:listar_ubicaciones_admin')
    else:
        form = UbicacionAdminForm(instance=ubicacion)
    return render(request, 'administrador/editar_ubicacion_admin.html', {'form': form, 'ubicacion': ubicacion})

# Eliminar ubicación
def eliminar_ubicacion_admin(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    if request.method == 'POST':
        ubicacion.delete()
        return redirect('administrador:listar_ubicaciones_admin')
    return render(request, 'administrador/eliminar_ubicacion_admin.html', {'ubicacion': ubicacion})