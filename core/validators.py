from django.core.exceptions import ValidationError


def limpiar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "").replace(" ", "")
    cuerpo = rut[:-1]
    dv = rut[-1]
    return cuerpo, dv


def calcular_dv(cuerpo):
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_rut(rut):
    try:
        cuerpo, dv = limpiar_rut(rut)
    except (IndexError, AttributeError):
        raise ValidationError("El RUT ingresado no es válido.")

    if not cuerpo.isdigit():
        raise ValidationError("El cuerpo del RUT debe contener solo números.")
    
    largo_normalizado = len(cuerpo) + 2  
    if largo_normalizado < 9 or largo_normalizado > 11:
        raise ValidationError(
            "El RUT debe tener entre 9 y 11 caracteres en formato 12345678-9."
        )

    if calcular_dv(cuerpo) != dv:
        raise ValidationError("El dígito verificador del RUT no es correcto.")
    
def normalizar_rut(rut):
    cuerpo, dv = limpiar_rut(rut)
    return f"{cuerpo}-{dv}"