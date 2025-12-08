def validar_rut(rut):
    """
    Valida un RUT chileno en formato string (con o sin puntos/guion).
    Retorna True si es válido, False si no.
    """
    rut = rut.replace('.', '').replace(' ', '').replace('-', '')
    if len(rut) < 2:
        return False
    cuerpo = rut[:-1]
    dv = rut[-1].lower()
    if not cuerpo.isdigit() or dv not in '0123456789k':
        return False
    suma = 0
    factor = 2
    for c in reversed(cuerpo):
        suma += int(c) * factor
        factor += 1
        if factor > 7:
            factor = 2
    res = 11 - (suma % 11)
    if res == 11:
        dv_esperado = '0'
    elif res == 10:
        dv_esperado = 'k'
    else:
        dv_esperado = str(res)
    return dv == dv_esperado
