from django.shortcuts import render
from django.http import HttpResponse

def lista_reportes(request):
    return HttpResponse('Listado de reportes (placeholder)')

def crear_reporte(request):
    return HttpResponse('Crear reporte (placeholder)')

def detalle_reporte(request, reporte_id):
    return HttpResponse(f'Detalle reporte {reporte_id} (placeholder)')

def editar_reporte(request, reporte_id):
    return HttpResponse(f'Editar reporte {reporte_id} (placeholder)')

def eliminar_reporte(request, reporte_id):
    return HttpResponse(f'Eliminar reporte {reporte_id} (placeholder)')
