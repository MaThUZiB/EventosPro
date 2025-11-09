from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            "tipo_evento",
            "nombre",
            "descripcion",
            "fecha",
            "hora",
            "ubicacion",
            "imagen",
            "precio",
            "stock",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "tipo_evento": forms.Select(attrs={"class": "bg-gray-700"}),
        }
