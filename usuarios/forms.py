from django import forms
from .models import Usuario
from .validators import validar_rut, validar_telefono_chileno
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ["username", "email", "rut", "telefono", "tipo_usuario"]
        widgets = {
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
            "rut": forms.TextInput(),
            "telefono": forms.TextInput(),
            "tipo_usuario": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_usuario'].choices = [
            ('', 'Seleccione un tipo de usuario'),
            ('cliente', 'Cliente'),
            ('organizador', 'Organizador'),
        ]

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

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        # Validar coincidencia
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        # Validar fortaleza de la contraseña
        if p1:
            try:
                validate_password(p1)
            except ValidationError as e:
                self.add_error("password1", e.messages)

        return cleaned_data
    
    def clean_tipo_usuario(self):
        tipo = self.cleaned_data.get("tipo_usuario")
        if not tipo:
            raise forms.ValidationError("Debe seleccionar un tipo de usuario.")
        return tipo
    
    
class InicioSesionForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
