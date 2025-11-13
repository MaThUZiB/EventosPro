from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from eventos.models import Evento

def registrar_usuario(request):
    if request.method == "GET":
        return render(request, "usuarios/registrar_usuario.html", {"form": RegistroUsuarioForm()})
    
    # POST
    form = RegistroUsuarioForm(request.POST)
    if form.is_valid():
        try:
            # Guardar usuario pero aún sin password
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["password1"])  # Tomamos password1 del form
            usuario.save()
            return redirect("iniciar_sesion")
        
        except IntegrityError:
            return render(request, "usuarios/registrar_usuario.html", {
                "form": form,
                "error": "El RUT o nombre de usuario ya existe."
            })
        except Exception as e:
            print(e)
            return render(request, "usuarios/registrar_usuario.html", {
                "form": form,
                "error": "Ocurrió un error al registrar el usuario."
            })
    else:
        print(form.errors)
        print(request.POST)
        return render(request, "usuarios/registrar_usuario.html", {
            "form": form,
            "error": "Datos inválidos en el formulario."
        })



def iniciar_sesion(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print("Authenticated user:", user)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirige a la página principal (home) después de iniciar sesión
        else:
            return render(request, "usuarios/iniciar_sesion.html",{
                'form': InicioSesionForm(),
                'error': 'Usuario o contraseña incorrectos.'
            })
    else:
        form = InicioSesionForm()
        return render(request, "usuarios/iniciar_sesion.html", {"form": form})
    


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


def home(request):
    evento = Evento.objects.filter(estado='publicado').order_by('fecha', 'hora')  # Obtener todos los eventos publicados
    return render(request, "usuarios/home.html", {
        'eventos': evento
    })

def acerca(request):
    return render(request, 'acerca.html')