from django import forms
from usuarios.models import Usuario
from eventos.models import Evento , Ubicacion
from usuarios.validators import validar_rut, validar_telefono_chileno
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

HOUR_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(8, 23)]

CLASES_INPUT = (
    "w-full px-4 py-2 rounded-lg bg-gray-800 text-white "
    "border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
)

class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "rut", "telefono", "tipo_usuario"]
        help_texts = {
    "username": "Ingresa un nombre único para el usuario."
}
        widgets = {
            "username": forms.TextInput(attrs={"class": CLASES_INPUT, "placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"class": CLASES_INPUT, "placeholder": "Correo electrónico"}),
            "rut": forms.TextInput(attrs={"class": CLASES_INPUT, "placeholder": "RUT"}),
            "telefono": forms.TextInput(attrs={"class": CLASES_INPUT, "placeholder": "Teléfono"}),
            "tipo_usuario": forms.Select(attrs={"class": CLASES_INPUT}),
        }
    # ---------------------------
    # VALIDACIONES PERSONALIZADAS
    # ---------------------------

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        validar_rut(rut)
        return rut
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        validar_telefono_chileno(telefono)
        return telefono

class EventoAdminForm(forms.ModelForm):
    hora = forms.ChoiceField(
        error_messages={
            "required": "Por favor, selecciona una hora para el evento.",
        },
        choices=HOUR_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
            }
        ),
    )

    class Meta:
        model = Evento
        fields = [
            "estado",
            "nombre",
            "descripcion",
            "fecha",
            "hora",
            "ubicacion",
            "imagen",
            "precio_ticket",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del evento",
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del evento (opcional)",
                    "rows": 4,
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none",
                }
            ),
            "fecha": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "ubicacion": forms.Select(
                attrs={
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "imagen": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100",
                }
            ),
            "precio_ticket": forms.NumberInput(
                attrs={
                    "min": 0,
                    "placeholder": "Precio del ticket",
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                }
            ),
        }

    def clean_precio_ticket(self):
        precio = self.cleaned_data.get("precio_ticket")
        if precio is None:
            raise forms.ValidationError("Debes ingresar un precio.")
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        if precio > 1000000:
            raise forms.ValidationError("El precio no puede superar 1 millón.")

        return precio
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < timezone.localdate():
            raise forms.ValidationError("No puedes crear eventos en fechas pasadas.")
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        hora_str = cleaned_data.get("hora")
        ubicacion = cleaned_data.get("ubicacion")

        if fecha and hora_str and ubicacion:
            # Convertir a objeto time
            try:
                hora = datetime.strptime(hora_str, "%H:%M").time()
            except ValueError:
                raise forms.ValidationError("Formato de hora inválido.")

            conflicto = Evento.objects.filter(
                fecha=fecha, hora=hora, ubicacion=ubicacion
            )

            if self.instance.pk:
                conflicto = conflicto.exclude(pk=self.instance.pk)

            if conflicto.exists():
                raise forms.ValidationError(
                    "Ya existe un evento programado en esta ubicación, fecha y hora."
                )

        return cleaned_data

class UbicacionAdminForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ["nombre", "direccion", "filas", "columnas", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": CLASES_INPUT, "placeholder": "Nombre de la ubicación"}),
            "direccion": forms.TextInput(attrs={"class": CLASES_INPUT, "placeholder": "Dirección"}),
            "filas": forms.NumberInput(attrs={"class": CLASES_INPUT, "min": 1}),
            "columnas": forms.NumberInput(attrs={"class": CLASES_INPUT, "min": 1}),
        }
    def clean(self):
        cleaned_data = super().clean()
        filas = cleaned_data.get("filas")
        columnas = cleaned_data.get("columnas")

        if filas <= 0 or filas > 100:
            self.add_error("filas", "Filas debe ser entre 1 y 100")
        if columnas <= 0 or columnas > 50:
            self.add_error("columnas", "Columnas debe ser entre 1 y 50")
