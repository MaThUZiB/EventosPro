from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "nombre",
            "descripcion",
            "fecha",
            "hora",
            "ubicacion",
            "imagen",
            "precio_ticket",
            "stock_ticket",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Nombre del evento"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "rows": 4,
                "placeholder": "Descripción del evento"
            }),
            "fecha": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "hora": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "ubicacion": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Ubicación del evento"
            }),
            "imagen": forms.ClearableFileInput(attrs={
                "class": "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            }),
            "precio_ticket": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "min": 0
            }),
            "stock_ticket": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "min": 0
            }),
        }
