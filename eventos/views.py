from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import EventoForm
from .models import Evento, AsientoEvento, Ubicacion
from compra.models import Compra, CompraDetalle, Pago


# Decorador
def es_organizador(user):
    return (
        user.is_authenticated and getattr(user, "tipo_usuario", None) == "organizador"
    )


# ---------------------------
# Vista AJAX para obtener asientos ocupados
# ---------------------------
@login_required
def obtener_asientos_ocupados(request, id):
    evento = get_object_or_404(Evento, id=id)
    ocupados = list(evento.asientos.filter(disponible=False).values_list('id', flat=True))
    return JsonResponse({"ocupados": ocupados}, safe=True)

# ---------------------------
# Vista principal para seleccionar asientos
# ---------------------------

@login_required
def seleccionar_asiento(request, id):
    evento = get_object_or_404(Evento, id=id)
    filas = evento.ubicacion.filas
    columnas = evento.ubicacion.columnas

    # Construir matriz de asientos
    asientos_qs = evento.asientos.all().order_by('fila', 'columna')
    seats_grid = [[None for _ in range(columnas)] for __ in range(filas)]
    for asiento in asientos_qs:
        r, c = asiento.fila - 1, asiento.columna - 1
        if 0 <= r < filas and 0 <= c < columnas:
            seats_grid[r][c] = asiento

    # Procesar compra
    if request.method == "POST":
        asientos_ids_str = request.POST.get("asientos_seleccionados", "")
        asientos_ids = [int(a) for a in asientos_ids_str.split(",") if a.strip().isdigit()]
        asientos_seleccionados = AsientoEvento.objects.filter(
            id__in=asientos_ids, evento=evento, disponible=True
        )

        if asientos_seleccionados.count() != len(asientos_ids):
            messages.error(request, "Algunos asientos ya no están disponibles.")
            return redirect('eventos:seleccionar_asiento', id=evento.id)

        # Crear compra y detalles
        total = evento.precio_ticket * len(asientos_seleccionados)
        compra = Compra.objects.create(usuario=request.user, total=total)

        for asiento in asientos_seleccionados:
            CompraDetalle.objects.create(compra=compra, asiento=asiento)
            asiento.disponible = False
            asiento.save()

        # Crear pago asociado (inicialmente pendiente)
        Pago.objects.create(compra=compra, metodo='Simulado', estado='pendiente')

        messages.success(request, "Compra creada. Procede a confirmar tu pago.")
        return redirect('compra:confirmar_compra', compra_id=compra.id)

    return render(request, 'eventos/seleccionar_asiento.html', {
        'evento': evento,
        'filas': filas,
        'columnas': columnas,
        'seats_grid': seats_grid,
    })


@login_required
@user_passes_test(es_organizador)
def obtener_horas_ocupadas(request):
    print(">>> FETCH RECIBIDO <<<")
    fecha = request.GET.get("fecha")
    ubicacion_id = request.GET.get("ubicacion")
    print("Fecha:", fecha)
    print("Ubicación:", ubicacion_id)

    horas_ocupadas = []

    if fecha and ubicacion_id:
        eventos = Evento.objects.filter(fecha=fecha, ubicacion_id=ubicacion_id)
        horas_ocupadas = [e.hora.strftime("%H:%M") for e in eventos]

    print("Horas ocupadas:", horas_ocupadas)

    # 🔹 devolvemos la lista bajo el nombre "ocupadas" y con encabezado JSON explícito
    return JsonResponse({"ocupadas": horas_ocupadas}, content_type="application/json")


# CREAR Evento
def generar_asientos_evento(evento):
    for fila in range(1, evento.ubicacion.filas + 1):
        for col in range(1, evento.ubicacion.columnas + 1):
            AsientoEvento.objects.create(
                evento=evento, fila=fila, columna=col, disponible=True
            )


@login_required
@user_passes_test(es_organizador)
def crear_evento(request):
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
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            generar_asientos_evento(evento)  # <- Genera los asientos automáticamente
            messages.success(request, "Evento creado correctamente.")
            return render(
                request,
                "eventos/mensaje_exito.html",
            )
    else:
        form = EventoForm()
    return render(
        request,
        "eventos/crear_eventos.html",
        {"form": form, "ubicaciones": ubicaciones},
    )


# LISTAR Eventos
def listar_eventos(request):
    eventos = Evento.objects.filter(estado="publicado").order_by("fecha", "hora")
    return render(request, "eventos/listar_eventos.html", {"eventos": eventos})


# DETALLE Eventos
def detalle_evento(request, id):
    evento = get_object_or_404(Evento.objects.select_related("ubicacion"), id=id)
    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
        },
    )


# EVENTOS POR ID
@login_required
@user_passes_test(es_organizador)
def mis_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    return render(request, "eventos/mis_eventos.html", {"eventos": eventos})


# EDITAR Eventos
@login_required
@user_passes_test(es_organizador)
def editar_evento(request, id):
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
    evento = get_object_or_404(Evento, id=id, usuario=request.user)
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente")
            return redirect("eventos:mis_eventos")
        else:
            messages.error(request, "Error al actualizar correctamente")
    else:
        form = EventoForm(instance=evento)
    return render(
        request,
        "eventos/editar_evento.html",
        {"form": form, "evento": evento, "ubicaciones": ubicaciones},
    )


# ELIMINAR Evento
@login_required
@user_passes_test(es_organizador)
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id, usuario=request.user)
    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento eliminado correctamente.")
        return redirect("eventos:mis_eventos")
    return render(request, "eventos/eliminar_evento.html", {"evento": evento})


# BUSQUEDA EVENTOS
def buscar_eventos(request):
    return render(request, "eventos/busqueda_eventos.html")


def buscar_eventos_ajax(request):
    q = request.GET.get("q", "")
    fecha = request.GET.get("fecha", "")

    resultados = Evento.objects.filter(estado="publicado")

    if q:
        resultados = resultados.filter(
            Q(nombre__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(ubicacion__nombre__icontains=q)
        )
    if fecha:
        resultados = resultados.filter(fecha=fecha)

    html = render_to_string(
        "eventos/resultados_busqueda.html", {"resultados": resultados}
    )
    return JsonResponse({"html": html})
