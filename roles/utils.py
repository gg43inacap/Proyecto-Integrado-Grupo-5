def validar_rut(rut):
    """
    Valida un RUT chileno en formato string (con o sin puntos/guion).
    Retorna True si es válido, False si no.
    """
    rut = rut.replace(".", "").replace(" ", "").replace("-", "")
    if len(rut) not in [9, 10]:
        return False
    if len(rut) == 9:
        rut = "0" + rut
    cuerpo = rut[:8]
    dv = rut[8:].lower()
    if not cuerpo.isdigit() or dv not in "0123456789k":
        return False
    tupla_factor = (3,2,7,6,5,4,3,2)
    suma = sum(int(cuerpo[i]) * tupla_factor[i] for i in range(8))
    residuo = suma % 11
    digito_verificador = 11 - residuo
    dv_esperado = "k" if digito_verificador == 10 else "0" if digito_verificador == 11 else str(digito_verificador)
    return dv == dv_esperado
