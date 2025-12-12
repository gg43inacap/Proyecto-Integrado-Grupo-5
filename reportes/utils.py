# reportes/utils.py
from datetime import date
from django.db.models import Q
from calendar import monthrange
from .models import RN  # Ajusta al nombre real de tu modelo

def get_reporte_rem24_completo(mes=None, anio=None, inicio=None, fin=None):
    """
    Devuelve todas las secciones del REM A24 filtradas por mes o rango de fechas.
    """

    # --- Normalización de fechas ---
    if mes and anio:
        start = date(anio, mes, 1)
        end = date(anio, mes, monthrange(anio, mes)[1])
    else:
        start = inicio
        end = fin

    filtro_tiempo = Q()
    if start and end:
        filtro_tiempo = Q(fecha_nacimiento__range=[start, end])  # Ajusta al campo real

    # --- Sección D.1: Información general RN vivos ---
    rn_vivos = RN.objects.filter(filtro_tiempo)
    seccion_d1 = {
        "titulo": "SECCIÓN D.1: Información general de recién nacidos vivos",
        "rows": [
            ["Menos de 500", rn_vivos.filter(peso__lt=500).count()],
            ["500 a 999", rn_vivos.filter(peso__gte=500, peso__lte=999).count()],
            ["1000 a 1499", rn_vivos.filter(peso__gte=1000, peso__lte=1499).count()],
            ["1500 a 1999", rn_vivos.filter(peso__gte=1500, peso__lte=1999).count()],
            ["2000 a 2499", rn_vivos.filter(peso__gte=2000, peso__lte=2499).count()],
            ["2500 a 2999", rn_vivos.filter(peso__gte=2500, peso__lte=2999).count()],
            ["3000 a 3999", rn_vivos.filter(peso__gte=3000, peso__lte=3999).count()],
            ["4000 y más", rn_vivos.filter(peso__gte=4000).count()],
            ["Total nacidos vivos", rn_vivos.count()],
            ["Anomalía congénita", rn_vivos.filter(anomalia_congenita=True).count()],
        ]
    }

    # --- Sección D.2: Atención inmediata RN ---
    seccion_d2 = {
        "titulo": "SECCIÓN D.2: Atención inmediata del recién nacido",
        "rows": [
            ["Profilaxis Hepatitis B", rn_vivos.filter(vacuna_hepatitis_b=True).count()],
            ["Profilaxis Ocular", rn_vivos.filter(profilaxis_ocular=True).count()],
            ["Parto Vaginal", rn_vivos.filter(parto_asociado__tipo_parto="vaginal").count()],
            ["Parto Instrumental", rn_vivos.filter(parto_asociado__tipo_parto="instrumental").count()],
            ["Cesárea", rn_vivos.filter(parto_asociado__tipo_parto__startswith="cesarea").count()],
            ["Parto extrahospitalario", rn_vivos.filter(parto_asociado__tipo_parto="extrahospitalario").count()],
            ["Apgar ≤ 3 al minuto", rn_vivos.filter(apgar_1__lte=3).count()],
            ["Apgar ≤ 6 a los 5 minutos", rn_vivos.filter(apgar_5__lte=6).count()],
            ["Reanimación Básica", rn_vivos.filter(reanimacion_basica=True).count()],
            ["Reanimación Avanzada", rn_vivos.filter(reanimacion_avanzada=True).count()],
            ["EHI Grado II y III", rn_vivos.filter(ehi_grado_ii_iii=True).count()],
            ["Distócico", rn_vivos.filter(parto_asociado__parto_distocico=True).count()],
            ["Vacuum", rn_vivos.filter(parto_asociado__parto_vacuum=True).count()],
            ["Cesárea Urgencia", rn_vivos.filter(parto_asociado__tipo_parto="cesarea_urgencia").count()],
            ["Cesárea Electiva", rn_vivos.filter(parto_asociado__tipo_parto="cesarea_electiva").count()],
            ["Total Partos", rn_vivos.count()],
        ]
    }


    # --- Sección D.3: Lactancia precoz ---
    rn_lactancia = rn_vivos.filter(peso__gte=2500, lactancia_antes_60=True)

    seccion_d3 = {
        "titulo": "SECCIÓN D.3: Lactancia materna en los primeros 60 minutos (RN ≥ 2500 g)",
        "rows": [
            ["Total Partos", rn_lactancia.count()],
            ["Vaginal", rn_lactancia.filter(parto_asociado__tipo_parto="vaginal").count()],
            ["Instrumental", rn_lactancia.filter(parto_asociado__tipo_parto="instrumental").count()],
            ["Cesárea Electiva", rn_lactancia.filter(parto_asociado__tipo_parto="cesarea_electiva").count()],
            ["Cesárea Urgencia", rn_lactancia.filter(parto_asociado__tipo_parto="cesarea_urgencia").count()],
        ]
    }
        # --- Retorno global ---
    periodo = f"{anio}-{mes:02d}" if mes and anio else (f"{inicio} a {fin}" if inicio and fin else "Sin filtro")
    return {
        "titulo": "REM A24 — Atención del Recién Nacido",
        "periodo": periodo,
        "seccion_d1": seccion_d1,
        "seccion_d2": seccion_d2,
        "seccion_d3": seccion_d3,
    }