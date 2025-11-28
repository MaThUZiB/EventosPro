from django import forms
from usuarios.models import Usuario
from eventos.models import Evento , Ubicacion

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

class EventoAdminForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["usuario", "ubicacion", "nombre", "descripcion", "fecha", "hora", "imagen", "estado", "precio_ticket"]
        widgets = {
            "usuario": forms.Select(attrs={"class": CLASES_INPUT}),
            "ubicacion": forms.Select(attrs={"class": CLASES_INPUT}),
            "nombre": forms.TextInput(attrs={"class": CLASES_INPUT}),
            "descripcion": forms.Textarea(attrs={"class": CLASES_INPUT, "rows": 3}),
            "fecha": forms.DateInput(attrs={"type": "date", "class": CLASES_INPUT}),
            "hora": forms.TimeInput(attrs={"type": "time", "class": CLASES_INPUT}),
            "imagen": forms.ClearableFileInput(attrs={"class": CLASES_INPUT}),
            "estado": forms.Select(attrs={"class": CLASES_INPUT}),
            "precio_ticket": forms.NumberInput(attrs={"class": CLASES_INPUT}),
        }

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

