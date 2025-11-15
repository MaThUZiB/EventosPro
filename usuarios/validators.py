import re
from django.core.exceptions import ValidationError

def validar_rut(rut):
    """
    Valida el RUT chileno (formato y dígito verificador).
    Acepta formatos con puntos o guiones.
    """

    rut = rut.upper().replace(".", "").replace("-", "")

    if not re.match(r'^\d+K?$', rut):
        raise ValidationError("El formato del RUT es inválido.")

    cuerpo = rut[:-1]
    dv = rut[-1]

    # Verificar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        raise ValidationError("El cuerpo del RUT debe ser numérico.")

    # --- Cálculo del dígito verificador ---
    suma = 0
    multiplicador = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    if dv != dv_calculado:
        raise ValidationError("El dígito verificador del RUT es incorrecto.")
