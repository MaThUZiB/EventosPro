from django import forms
from .models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    # Campos extra que no están en el modelo
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ["username", "email", "rut", "telefono", "tipo_usuario"]  # sin password1/2
        widgets = {
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
            "rut": forms.TextInput(),
            "telefono": forms.TextInput(),
            "tipo_usuario": forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo permitir cliente u organizador en el formulario público
        self.fields['tipo_usuario'].choices = [
            ('cliente', 'Cliente'),
            ('organizador', 'Organizador'),
        ]

    # Validación de contraseña
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
class InicioSesionForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
