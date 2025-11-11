from django import forms
from .models import Evento
from datetime import datetime
from django.utils import timezone

HOUR_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(8, 23)]


class EventoForm(forms.ModelForm):
    hora = forms.ChoiceField(
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
                    "placeholder": "Descripción del evento",
                    "rows": 4,
                    "class": "w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none",
                }
            ),
            "fecha": forms.DateInput(
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
        }

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
