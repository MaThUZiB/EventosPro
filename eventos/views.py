from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test 
from django.http import HttpResponse
from .forms import EventoForm
from .models import Evento, Funcion, Sala, Butaca, Ticket, Sector
from django.contrib import messages

def es_organizador(user):
    return user.is_authenticated and getattr(user, "tipo_usuario", None) == "organizador"

# --------- ORGANIZADOR (lo que ya tenías) ---------
@user_passes_test(es_organizador)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()

            # ✅ Crear función automáticamente usando los datos del evento
            Funcion.objects.create(
                evento=evento,
                fecha=evento.fecha,
                hora=evento.hora,
                lugar=evento.ubicacion  # usamos el campo ubicacion del evento
            )
            return render(request, 'eventos/mensaje_exito.html',)
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_eventos.html', {'form': form})


@user_passes_test(es_organizador)
def editar_evento(request, id):
    from .forms import EventoForm
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('mis_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

@user_passes_test(es_organizador)
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('mis_eventos')
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

@user_passes_test(es_organizador)
def mis_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    return render(request, 'eventos/mis_eventos.html', {'eventos': eventos})

# --------- PÚBLICO ---------
def listar_eventos(request):
    eventos = Evento.objects.filter(estado='publicado').order_by('fecha', 'hora')
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})

def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    funciones = Funcion.objects.filter(evento=evento).order_by('fecha', 'hora')

    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
        'funciones': funciones
    })

def listar_tickets(request):
    tickets = Ticket.objects.filter(usuario=request.user)
    return render(request, 'eventos/listar_tickets.html', {'tickets': tickets})


def seleccionar_butacas(request, funcion_id):
    funcion = get_object_or_404(Funcion, id=funcion_id)
    sala = Sala.objects.filter(funcion=funcion).first()
    butacas = Butaca.objects.filter(sala=sala).order_by('fila', 'numero')

    if request.method == "POST":
        seleccionadas = request.POST.getlist("butacas")
        if seleccionadas:
            ids = ",".join(seleccionadas)
            return redirect(f"/eventos/checkout/?butacas={ids}")

    return render(request, "eventos/seleccionar_butacas.html", {
        "funcion": funcion,
        "sala": sala,
        "butacas": butacas
    })


def checkout(request):
    """Recibe ?sector=ID (fiestas) o ?butacas=1,2,3 (cine)."""
    sector_id = request.GET.get("sector")
    butacas_ids = request.GET.get("butacas")

    if sector_id:
        sector = get_object_or_404(Sector, id=sector_id)
        evento = sector.funcion.evento
        total = sector.precio
        return render(request, "eventos/checkout_general.html", {
            "evento": evento,
            "sector": sector,
            "total": total
        })

    if butacas_ids:
        ids = [x for x in butacas_ids.split(",") if x]
        butacas = Butaca.objects.filter(id__in=ids)
        if not butacas:
            return redirect('home')
        funcion = butacas.first().sala.funcion
        precio = funcion.evento.precio or 0
        total = precio * len(butacas)
        return render(request, "eventos/checkout.html", {
            "funcion": funcion,
            "butacas": butacas,
            "precio": precio,
            "total": total
        })

    # Si llega sin parámetros, reenvía al home o detalle
    return redirect('home')

@csrf_exempt
def comprar_invitado(request):
    """Procesa la compra de entradas para usuarios o invitados (según autenticación)."""
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect("eventos:listar_eventos")

    email = request.POST.get("email", "").strip()
    cantidad = int(request.POST.get("cantidad", "1"))
    sector_id = request.POST.get("sector")
    butacas_ids = request.POST.get("butacas")

    # Determinar si el usuario está autenticado
    if request.user.is_authenticated:
        usuario = request.user
        correo = request.user.email
    else:
        usuario = None
        correo = email

    # Validar correo si es invitado
    if not correo:
        messages.error(request, "Debes ingresar un correo electrónico válido.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Compra por sector (fiesta/concierto)
    if sector_id:
        sector = get_object_or_404(Sector, id=sector_id)
        for _ in range(cantidad):
            Ticket.objects.create(
                usuario=usuario,
                invitado_email=None if usuario else correo,
                funcion=sector.funcion,
                sector=sector,
                precio=sector.precio,
                pagado=True
            )
        messages.success(request, f"Compra realizada con éxito 🎟️. Se enviarán las entradas a {correo}.")
        return render(request, "eventos/compra_exitosa.html")

    # Compra por butacas (cine/teatro)
    if butacas_ids:
        ids = [x for x in butacas_ids.split(",") if x]
        for bid in ids:
            b = get_object_or_404(Butaca, id=bid)
            Ticket.objects.create(
                usuario=usuario,
                invitado_email=None if usuario else correo,
                funcion=b.sala.funcion,
                butaca=b,
                precio=b.sala.funcion.evento.precio,
                pagado=True
            )
            b.disponible = False
            b.save()
        messages.success(request, f"Compra realizada con éxito 🎟️. Se enviarán las entradas a {correo}.")
        return render(request, "eventos/compra_exitosa.html")

    # Si no hay sector ni butacas
    messages.error(request, "No se ha seleccionado un sector ni butacas.")
    return redirect("eventos:listar_eventos")