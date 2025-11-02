from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import EventoForm
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


def es_organizador(user):
    return user.is_authenticated and user.tipo_usuario == 'organizador'

@user_passes_test(es_organizador)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_eventos.html', {
        'form': form
    })

@user_passes_test(es_organizador)
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id= id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('mis_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/editar_evento.html', {
        'form': form,
        'evento': evento
    })

@user_passes_test(es_organizador)
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('mis_eventos')
    return render(request, 'eventos/eliminar_evento.html', {
        'evento':evento    
    })

@user_passes_test(es_organizador)
def mis_eventos(request):
    eventos = Evento.objects.filter(usuario=request.user)
    return render(request, 'eventos/mis_eventos.html', {'eventos': eventos})

def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'eventos/detalle_evento.html', {'evento': evento})