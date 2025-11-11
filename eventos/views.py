from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import EventoForm
from .models import Evento

#Decorador
def es_organizador(user):
    return user.is_authenticated and getattr(user, "tipo_usuario", None) == "organizador"

#CREAR Evento
@login_required
@user_passes_test(es_organizador)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            messages.success(request, "Evento creado correctamente.")
            return render(request, 'eventos/mensaje_exito.html',)
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_eventos.html', {'form': form})

#LISTAR Eventos
def listar_eventos(request):
    eventos = Evento.objects.filter(estado='publicado').order_by('fecha', 'hora')
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})

#DETALLE Eventos
def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
    })

#EVENTOS POR ID
@login_required
@user_passes_test(es_organizador)
def mis_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    return render(request, 'eventos/mis_eventos.html', {'eventos': eventos})

#EDITAR Eventos
@login_required
@user_passes_test(es_organizador)
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id, usuario=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente")
            return redirect('eventos:mis_eventos')
        else:
            messages.error(request, "Error al actualizar correctamente")
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})

#ELIMINAR Evento
@login_required
@user_passes_test(es_organizador)
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id, usuario=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento eliminado correctamente.")
        return redirect('mis_eventos')
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})

#BUSQUEDA EVENTOS
def buscar_eventos(request):
    return render(request, 'eventos/busqueda_eventos.html')

def buscar_eventos_ajax(request):
    q = request.GET.get('q', '')
    fecha = request.GET.get('fecha', '')

    resultados = Evento.objects.filter(estado='publicado')

    if q:
        resultados = resultados.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(ubicacion__icontains=q)
        )
    if fecha:
        resultados = resultados.filter(fecha=fecha)

    html = render_to_string('eventos/resultados_busqueda.html', {'resultados': resultados})
    return JsonResponse({'html': html})






