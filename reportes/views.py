from django.shortcuts import render # Mostrar páginas
from django.http import HttpResponse # Responder texto plano
from django.db.models import Count, Q
from partos.models import Parto, RN
from .exportadores import (exportar_reporte_parto_pdf, exportar_reporte_parto_excel,
                            exportar_reporte_nacidos_vivos_pdf, exportar_reporte_nacidos_vivos_excel,
                            exportar_reporte_atencion_inmediata_pdf, exportar_reporte_atencion_inmediata_excel)




def reporte_parto(request):
    # Total partos por tipo
    total_partos = Parto.objects.count()
    vaginal = Parto.objects.filter(tipo_parto="vaginal").count()
    instrumental = Parto.objects.filter(tipo_parto="instrumental").count()
    cesarea_electiva = Parto.objects.filter(tipo_parto="cesarea_electiva").count()
    cesarea_urgencia = Parto.objects.filter(tipo_parto="cesarea_urgencia").count()

    # RN ≥ 2500 g con lactancia precoz por tipo de parto
    rn_filtrados = RN.objects.filter(peso__gte=2500, lactancia_antes_60=True)
    total_lactancia = rn_filtrados.count()
    lactancia_vaginal = rn_filtrados.filter(parto_asociado__tipo_parto="vaginal").count()
    lactancia_instrumental = rn_filtrados.filter(parto_asociado__tipo_parto="instrumental").count()
    lactancia_electiva = rn_filtrados.filter(parto_asociado__tipo_parto="cesarea_electiva").count()
    lactancia_urgencia = rn_filtrados.filter(parto_asociado__tipo_parto="cesarea_urgencia").count()


    # Construimos la tabla con dos columnas
    data = {
        "headers": [
            "Características del Parto",
            "Lactancia materna en los primeros 60 minutos (RN ≥ 2500 g)"
        ],
        "rows": [
            ["Total Partos", total_lactancia],
            ["Vaginal", lactancia_vaginal],
            ["Instrumental", lactancia_instrumental],
            ["Cesárea Electiva", lactancia_electiva],
            ["Cesárea Urgencia", lactancia_urgencia],
        ],
        "reporte_nombre": "reporte_parto",
    }
    return render(request, "reportes/predefinidos/rem_24_caracteristicas_parto.html", {"data": data})


def reporte_nacidos_vivos(request):
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
        ],
        # Antes: "rem_a24_info_gral_rn_vivos"
        "reporte_nombre": "reporte_nacidos_vivos",
    }
    return render(request, "reportes/predefinidos/rem_a24_info_gral_rn_vivos.html", {"data": data})


def reporte_atencion_inmediata(request):
    data = {
        "headers": ["Indicador", "Cantidad"],
        "rows": [
            ["Total nacidos vivos", RN.objects.count()],
            ["Profilaxis Hepatitis B", RN.objects.filter(vacuna_hepatitis_b=True).count()],
            ["Profilaxis Ocular", RN.objects.filter(profilaxis_ocular=True).count()],
            ["Parto Vaginal", Parto.objects.filter(tipo_parto="vaginal").count()],
            ["Parto Instrumental", Parto.objects.filter(tipo_parto="instrumental").count()],
            ["Cesárea", Parto.objects.filter(tipo_parto__in=["cesarea_electiva", "cesarea_urgencia"]).count()],
            ["Parto Extrahospitalario", Parto.objects.filter(tipo_parto="extrahospitalario").count()],
            ["Apgar ≤ 3 al minuto", RN.objects.filter(apgar_1__lte=3).count()],
            ["Apgar ≤ 6 a los 5 minutos", RN.objects.filter(apgar_5__lte=6).count()],
            ["Reanimación Básica", RN.objects.filter(reanimacion_basica=True).count()],
            ["Reanimación Avanzada", RN.objects.filter(reanimacion_avanzada=True).count()],
            ["EHI Grado II y III", RN.objects.filter(ehi_grado_ii_iii=True).count()],
        ],
        # Antes: "rem_a24_atencion_inmediata_rn"
        "reporte_nombre": "reporte_atencion_inmediata",
    }
    return render(request, "reportes/predefinidos/rem_a24_atencion_inmediata_rn.html", {"data": data})


def panel_supervisor(request):
    return render(request, "roles/panel_supervisor.html")

def selector_de_reportes(request):
    return render(request, "reportes/componentes/selector_reportes.html")  # pantalla donde eliges qué reporte ver

def selector_de_filtros(request):
    return render(request, "reportes/componentes/selector_filtros.html")  # placeholder (lo llenamos luego)



def exportar_reporte(request):
    if request.method == 'POST':
        formato = request.POST.get('formato')
        reporte = request.POST.get('reporte')
        print("Recibido:", reporte, "como", formato)
        if reporte == 'reporte_parto':
            if formato == 'pdf':
                return exportar_reporte_parto_pdf(request)
            elif formato == 'excel':
                return exportar_reporte_parto_excel(request)

        elif reporte == 'reporte_nacidos_vivos':
            if formato == 'pdf':
                return exportar_reporte_nacidos_vivos_pdf(request)
            elif formato == 'excel':
                return exportar_reporte_nacidos_vivos_excel(request)
        elif reporte == 'reporte_atencion_inmediata':
            if formato == 'pdf':
                return exportar_reporte_atencion_inmediata_pdf(request)
            elif formato == 'excel':
                return exportar_reporte_atencion_inmediata_excel(request)

        return HttpResponse("Reporte o formato no válido", status=400)

    return HttpResponse("Método no permitido", status=405)