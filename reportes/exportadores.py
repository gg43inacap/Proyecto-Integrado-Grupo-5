import io
import openpyxl
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Parto, RN

# === REPORTE 1: Características del Parto ===

def exportar_reporte_parto_pdf(request):
    data = {
        "headers": ["Tipo de Parto", "Cantidad"],
        "rows": [
            ["Total Partos", Parto.objects.count()],
            ["Vaginal", Parto.objects.filter(tipo_parto="vaginal").count()],
            ["Instrumental", Parto.objects.filter(tipo_parto="instrumental").count()],
            ["Cesárea Electiva", Parto.objects.filter(tipo_parto="cesarea_electiva").count()],
            ["Cesárea Urgencia", Parto.objects.filter(tipo_parto="cesarea_urgencia").count()],
            ["Lactancia precoz (≥2500 g)", RN.objects.filter(peso__gte=2500, lactancia_antes_60=True).count()],
        ]
    }

    html = render_to_string("reportes/exportables/rem_24_caracteristicas_parto_pdf.html", {"data": data})
    result = io.BytesIO()
    pisa.CreatePDF(html, dest=result)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_parto.pdf"'
    return response


def exportar_reporte_parto_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Características del Parto"

    headers = ["Tipo de Parto", "Cantidad"]
    rows = [
        ["Total Partos", Parto.objects.count()],
        ["Vaginal", Parto.objects.filter(tipo_parto="vaginal").count()],
        ["Instrumental", Parto.objects.filter(tipo_parto="instrumental").count()],
        ["Cesárea Electiva", Parto.objects.filter(tipo_parto="cesarea_electiva").count()],
        ["Cesárea Urgencia", Parto.objects.filter(tipo_parto="cesarea_urgencia").count()],
        ["Lactancia precoz (≥2500 g)", RN.objects.filter(peso__gte=2500, lactancia_antes_60=True).count()],
    ]

    ws.append(headers)
    for row in rows:
        ws.append(row)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="reporte_parto.xlsx"'
    wb.save(response)
    return response


# === REPORTE 2: Información general RN vivos ===

def exportar_reporte_nacidos_vivos_pdf(request):
    data = {
        "headers": ["Rango de Peso (g)", "Cantidad"],
        "rows": [
            ["Menos de 500", RN.objects.filter(peso__lt=500).count()],
            ["500 a 999", RN.objects.filter(peso__gte=500, peso__lte=999).count()],
            ["1.000 a 1.499", RN.objects.filter(peso__gte=1000, peso__lte=1499).count()],
            ["1.500 a 1.999", RN.objects.filter(peso__gte=1500, peso__lte=1999).count()],
            ["2.000 a 2.499", RN.objects.filter(peso__gte=2000, peso__lte=2499).count()],
            ["2.500 a 2.999", RN.objects.filter(peso__gte=2500, peso__lte=2999).count()],
            ["3.000 a 3.999", RN.objects.filter(peso__gte=3000, peso__lte=3999).count()],
            ["4.000 y más", RN.objects.filter(peso__gte=4000).count()],
            ["Total nacidos vivos", RN.objects.count()],
            ["Con anomalía congénita", RN.objects.filter(anomalia_congenita=True).count()],
        ]
    }

    html = render_to_string("reportes/exportables/rem_a24_info_gral_rn_vivos_pdf.html", {"data": data})
    result = io.BytesIO()
    pisa.CreatePDF(html, dest=result)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_nacidos_vivos.pdf"'
    return response


def exportar_reporte_nacidos_vivos_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Info RN Vivos"

    headers = ["Rango de Peso (g)", "Cantidad"]
    rows = [
        ["Menos de 500", RN.objects.filter(peso__lt=500).count()],
        ["500 a 999", RN.objects.filter(peso__gte=500, peso__lte=999).count()],
        ["1.000 a 1.499", RN.objects.filter(peso__gte=1000, peso__lte=1499).count()],
        ["1.500 a 1.999", RN.objects.filter(peso__gte=1500, peso__lte=1999).count()],
        ["2.000 a 2.499", RN.objects.filter(peso__gte=2000, peso__lte=2499).count()],
        ["2.500 a 2.999", RN.objects.filter(peso__gte=2500, peso__lte=2999).count()],
        ["3.000 a 3.999", RN.objects.filter(peso__gte=3000, peso__lte=3999).count()],
        ["4.000 y más", RN.objects.filter(peso__gte=4000).count()],
        ["Total nacidos vivos", RN.objects.count()],
        ["Con anomalía congénita", RN.objects.filter(anomalia_congenita=True).count()],
    ]

    ws.append(headers)
    for row in rows:
        ws.append(row)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="reporte_nacidos_vivos.xlsx"'
    wb.save(response)
    return response


# === REPORTE 3: Atención inmediata RN ===

def exportar_reporte_atencion_inmediata_pdf(request):
    data = {
        "headers": ["Indicador", "Cantidad"],
        "rows": [
            ["Total nacidos vivos", RN.objects.count()],
            ["Profilaxis Hepatitis B", RN.objects.filter(vacuna_hepatitis_b=True).count()],
            ["Profilaxis Ocular", RN.objects.filter(profilaxis_ocular=True).count()],
            ["Parto Vaginal", Parto.objects.filter(tipo_parto="vaginal").count()],
            ["Parto Instrumental", Parto.objects.filter(tipo_parto="instrumental").count()],
            ["Cesárea", Parto.objects.filter(tipo_parto__startswith="cesarea").count()],
            ["Parto Extrahospitalario", Parto.objects.filter(tipo_parto="extrahospitalario").count()],
            ["Apgar ≤ 3 al minuto", RN.objects.filter(apgar_1__lte=3).count()],
            ["Apgar ≤ 6 a los 5 minutos", RN.objects.filter(apgar_5__lte=6).count()],
            ["Reanimación Básica", RN.objects.filter(reanimacion_basica=True).count()],
            ["Reanimación Avanzada", RN.objects.filter(reanimacion_avanzada=True).count()],
            ["EHI Grado II y III", RN.objects.filter(ehi_grado_ii_iii=True).count()],
        ]
    }

    html = render_to_string("reportes/exportables/rem_a24_atencion_inmediata_rn_pdf.html", {"data": data})
    result = io.BytesIO()
    pisa.CreatePDF(html, dest=result)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporte_atencion_inmediata.pdf"'
    return response


def exportar_reporte_atencion_inmediata_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Atención Inmediata RN"

    headers = ["Indicador", "Cantidad"]
    rows = [
        ["Total nacidos vivos", RN.objects.count()],
        ["Profilaxis Hepatitis B", RN.objects.filter(vacuna_hepatitis_b=True).count()],
        ["Profilaxis Ocular", RN.objects.filter(profilaxis_ocular=True).count()],
        ["Parto Vaginal", Parto.objects.filter(tipo_parto="vaginal").count()],
        ["Parto Instrumental", Parto.objects.filter(tipo_parto="instrumental").count()],
        ["Cesárea", Parto.objects.filter(tipo_parto__startswith="cesarea").count()],
        ["Parto Extrahospitalario", Parto.objects.filter(tipo_parto="extrahospitalario").count()],
        ["Apgar ≤ 3 al minuto", RN.objects.filter(apgar_1__lte=3).count()],
        ["Apgar ≤ 6 a los 5 minutos", RN.objects.filter(apgar_5__lte=6).count()],
        ["Reanimación Básica", RN.objects.filter(reanimacion_basica=True).count()],
        ["Reanimación Avanzada", RN.objects.filter(reanimacion_avanzada=True).count()],
        ["EHI Grado II y III", RN.objects.filter(ehi_grado_ii_iii=True).count()],
    ]

    ws.append(headers)
    for row in rows:
        ws.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="reporte_atencion_inmediata.xlsx"'
    wb.save(response)
    return response