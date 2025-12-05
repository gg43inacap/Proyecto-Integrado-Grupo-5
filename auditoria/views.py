from django.shortcuts import render
from django.http import HttpResponse

def lista_auditorias(request):
    return HttpResponse('Listado de auditorias (placeholder)')

def crear_auditoria(request):
    return HttpResponse('Crear auditoria (placeholder)')

def detalle_auditoria(request, auditoria_id):
    return HttpResponse(f'Detalle auditoria {auditoria_id} (placeholder)')

def editar_auditoria(request, auditoria_id):
    return HttpResponse(f'Editar auditoria {auditoria_id} (placeholder)')

def eliminar_auditoria(request, auditoria_id):
    return HttpResponse(f'Eliminar auditoria {auditoria_id} (placeholder)')
