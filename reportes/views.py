# reportes/views.py
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from .utils import get_reporte_rem24_completo
from django.template.loader import render_to_string
import io
from xhtml2pdf import pisa
from django.shortcuts import render
from datetime import datetime

def exportar_rem_a24_excel(request):
    # --- Capturar filtros desde GET ---
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")
    inicio = request.GET.get("inicio")
    fin = request.GET.get("fin")

    mes = int(mes) if mes else None
    anio = int(anio) if anio else None
    inicio = date.fromisoformat(inicio) if inicio else None
    fin = date.fromisoformat(fin) if fin else None

    # --- Obtener datos del reporte ---
    data = get_reporte_rem24_completo(mes=mes, anio=anio, inicio=inicio, fin=fin)

    # --- Crear Excel ---
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "REM A24"

    # Estilos
    bold = Font(bold=True)
    center = Alignment(horizontal="center")
    header_fill = PatternFill("solid", fgColor="F2F2F2")
    thin = Border(left=Side(style="thin"), right=Side(style="thin"),
                  top=Side(style="thin"), bottom=Side(style="thin"))

    # Título y periodo
    ws["A1"] = data["titulo"]
    ws["A2"] = f"Periodo: {data['periodo']}"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"].font = Font(bold=True)

    row_start = 4

    # --- Sección D.1 ---
    ws[f"A{row_start}"] = data["seccion_d1"]["titulo"]
    ws[f"A{row_start}"].font = bold
    row_start += 1
    for row in data["seccion_d1"]["rows"]:
        ws.append(row)
    row_start = ws.max_row + 2

    # --- Sección D.2 ---
    ws[f"A{row_start}"] = data["seccion_d2"]["titulo"]
    ws[f"A{row_start}"].font = bold
    row_start += 1
    for row in data["seccion_d2"]["rows"]:
        ws.append(row)
    row_start = ws.max_row + 2

    # --- Sección D.3 ---
    ws[f"A{row_start}"] = data["seccion_d3"]["titulo"]
    ws[f"A{row_start}"].font = bold
    row_start += 1
    for row in data["seccion_d3"]["rows"]:
        ws.append(row)

    # Ajustar ancho de columnas
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 20

    # --- Respuesta HTTP ---
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="REM_A24_{data["periodo"]}.xlsx"'
    wb.save(response)
    return response

def exportar_rem_a24_pdf(request):
    # --- Capturar filtros desde POST o GET ---
    mes = request.POST.get("mes") or request.GET.get("mes")
    anio = request.POST.get("anio") or request.GET.get("anio")
    inicio = request.POST.get("inicio") or request.GET.get("inicio")
    fin = request.POST.get("fin") or request.GET.get("fin")

    mes = int(mes) if mes else None
    anio = int(anio) if anio else None
    inicio = date.fromisoformat(inicio) if inicio else None
    fin = date.fromisoformat(fin) if fin else None

    # --- Obtener datos del reporte ---
    data = get_reporte_rem24_completo(mes=mes, anio=anio, inicio=inicio, fin=fin)

    # --- Renderizar template HTML ---
    html = render_to_string("reportes/exportable_rem_a24.html", {
        "titulo": data["titulo"],
        "periodo": data["periodo"],
        "seccion_d1": data["seccion_d1"],
        "seccion_d2": data["seccion_d2"],
        "seccion_d3": data["seccion_d3"],
    })

    # --- Convertir a PDF ---
    result = io.BytesIO()
    pisa.CreatePDF(html, dest=result)

    # --- Respuesta HTTP ---
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="REM_A24_{data["periodo"]}.pdf"'
    return response

def rem_24(request):
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")

    now = datetime.now()
    mes = int(mes) if mes else now.month
    anio = int(anio) if anio else now.year

    # Diccionario de meses en español
    meses_nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    periodo_legible = f"{meses_nombres[mes]} {anio}"

    data = get_reporte_rem24_completo(mes=mes, anio=anio)

    lista_anios = range(now.year - 5, now.year + 1)

    return render(request, "reportes/rem_24.html", {
        "titulo": data["titulo"],
        "periodo": periodo_legible,  # usamos el texto legible
        "seccion_d1": data["seccion_d1"],
        "seccion_d2": data["seccion_d2"],
        "seccion_d3": data["seccion_d3"],
        "lista_anios": lista_anios,
        "mes_seleccionado": mes,
        "anio_seleccionado": anio,
    })