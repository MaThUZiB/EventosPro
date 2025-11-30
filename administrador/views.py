from django.shortcuts import render , get_object_or_404, redirect
from compra.models import Compra 
from usuarios.models import Usuario
from eventos.models import Evento, Ubicacion
from .forms import UsuarioAdminForm, EventoAdminForm, UbicacionAdminForm
from django.contrib import messages
from django.db.models import Q ,Sum, ProtectedError

# Create your views here.
def admin_inicio(request):
    ingresos_totales = Compra.objects.filter(estado='completada').aggregate(Sum('total'))['total__sum'] or 0
    compras_completadas = Compra.objects.filter(estado='completada').count()
    compras_canceladas = Compra.objects.filter(estado='cancelada').count()
    ubicaciones_totales = Ubicacion.objects.count()
    eventos_pendientes = Evento.objects.filter(estado = 'pendiente').count()
    eventos_activos = Evento.objects.filter(estado = 'publicado').count()
    usuarios_totales = Usuario.objects.count()
    entradas_vendidas = Compra.objects.count()
    return render(request, 'administrador/admin_inicio.html', {
        'eventos_pendientes': eventos_pendientes,
        'eventos_activos': eventos_activos,
        'usuarios_totales': usuarios_totales,
        'entradas_vendidas': entradas_vendidas,
        'ubicaciones_totales': ubicaciones_totales,
        'compras_completadas': compras_completadas,
        'compras_canceladas': compras_canceladas,
        'ingresos_totales': ingresos_totales,
    })

def listar_usuarios_admin(request):
    q = request.GET.get("q", "")

    if q:
        usuarios = Usuario.objects.filter(username__icontains=q)
    else:
        usuarios = Usuario.objects.all()

    return render(request, "administrador/listar_usuarios_admin.html", {
        "usuarios": usuarios
    })

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
    q = request.GET.get("q", "")

    if q:
        eventos = Evento.objects.filter(nombre__icontains=q).order_by("-id")
    else:
        eventos = Evento.objects.all().order_by("-id")
    return render(request, "administrador/listar_eventos_admin.html", {"eventos": eventos})

def editar_evento_admin(request, id):
    ubicaciones_qs = Ubicacion.objects.all()
    ubicaciones = [
        {
            "id": u.id,
            "nombre": u.nombre,
            "direccion": u.direccion,
            "capacidad": u.capacidad(),
            "imagen": u.imagen.url if u.imagen else "",
        }
        for u in ubicaciones_qs
    ]
    evento = get_object_or_404(Evento, id=id)
    if request.method == "POST":
        form = EventoAdminForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente")
            return redirect("administrador:listar_eventos_admin")
        else:
            messages.error(request, "Error al actualizar correctamente")
    else:
        form = EventoAdminForm(instance=evento)
    return render(request, "administrador/editar_evento_admin.html", {"form": form, "evento": evento, "ubicaciones": ubicaciones})

def eliminar_evento_admin(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento eliminado correctamente")
        return redirect("administrador:listar_eventos_admin")
    return render(request, "administrador/eliminar_evento_admin.html", {"evento": evento})

# Listar compras para admin
def listar_compras_admin(request):
    q = request.GET.get("q", "")

    compras = Compra.objects.select_related('usuario', 'evento_id').prefetch_related('detalles', 'pago')

    if q:
        compras = compras.filter(
            Q(usuario__username__icontains=q) |
            Q(usuario__first_name__icontains=q) |
            Q(usuario__last_name__icontains=q) |
            Q(evento_id__nombre__icontains=q) |
            Q(asientos_nombres__icontains=q) |
            Q(total__icontains=q) |
            Q(fecha__date__icontains=q) |
            Q(pago__estado__icontains=q)
        )
    # --- Totales por estado ---
    total_general_completados = compras.filter(estado='completada').aggregate(Sum('total'))['total__sum'] or 0
    total_general_cancelados = compras.filter(estado='cancelada').aggregate(Sum('total'))['total__sum'] or 0
    compras = compras.order_by('-fecha')

    return render(request, 'administrador/listar_compras_admin.html', {
        'compras': compras,
        'total_general_completados': total_general_completados,
        'total_general_cancelados': total_general_cancelados,
    })


# Ver detalle de una compra
def ver_compra_admin(request, compra_id):
    compra = get_object_or_404(Compra.objects.select_related('usuario').prefetch_related('detalles', 'pago'), pk=compra_id)
    return render(request, 'administrador/ver_compra_admin.html', {'compra': compra})

# Eliminar compra
def eliminar_compra_admin(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    if request.method == "POST":
        compra.cancelar()
        messages.success(request, "Compra cancelada correctamente.")
        return redirect('administrador:listar_compras_admin')
    return render(request, 'administrador/eliminar_compra_admin.html', {'compra': compra})

# Listar todas las ubicaciones
def listar_ubicaciones_admin(request):
    q = request.GET.get("q", "")
    if q:
        ubicaciones = Ubicacion.objects.filter(nombre__icontains=q)
    else:
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
from django.contrib import messages

def eliminar_ubicacion_admin(request, id):
    ubicacion = get_object_or_404(Ubicacion, pk=id)

    if request.method == "POST":
        try:
            ubicacion.delete()
            messages.success(request, f"La ubicación {ubicacion.nombre} fue eliminada correctamente.")
            return redirect("administrador:listar_ubicaciones_admin")
        except ProtectedError:
            messages.error(request, "No se puede eliminar la ubicación porque hay eventos asociados.")
            return render(request, "administrador/eliminar_ubicacion_admin.html", {"ubicacion": ubicacion, "error": "No se puede eliminar la ubicación porque hay eventos asociados."})
    return render(request, "administrador/eliminar_ubicacion_admin.html", {"ubicacion": ubicacion})
    
def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, 'administrador/detalle_usuario.html', {'usuario': usuario})

def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'administrador/detalle_evento.html', {'evento': evento})

def detalle_ubicacion(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    capacidad = ubicacion.capacidad()
    return render(request, 'administrador/detalle_ubicacion.html', {'ubicacion': ubicacion, 'capacidad': capacidad})