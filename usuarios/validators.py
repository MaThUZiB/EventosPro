import re
from django.core.exceptions import ValidationError


def validar_rut(value):
    import re
    from django.core.exceptions import ValidationError

    rut = value.upper().replace(".", "").replace("-", "")

    if not re.match(r"^\d+[0-9K]$", rut):
        raise ValidationError("Formato de RUT inválido.")

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2

    # Multiplicadores correctos: 2 → 3 → 4 → 5 → 6 → 7 → (vuelve a 2)
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    dv_calc = 11 - (suma % 11)
    dv_calc = "0" if dv_calc == 11 else "K" if dv_calc == 10 else str(dv_calc)

    if dv != dv_calc:
        raise ValidationError("RUT inválido (dígito verificador incorrecto).")


def validar_telefono_chileno(value):
    numero = value.replace(" ", "").replace("+", "")

    if not re.match(r"^(56)?9\d{8}$", numero):
        raise ValidationError(
            "El número debe ser chileno, comenzar con +569 o 569 y tener 9 dígitos."
        )
