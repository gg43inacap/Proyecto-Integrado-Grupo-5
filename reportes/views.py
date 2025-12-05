from django.shortcuts import render # Mostrar páginas
from django.http import HttpResponse # Responder texto plano

# Las siguientes vistas son placeholders para el CRUD de reportes
# Se pueden modificar para agregar lógica real según las necesidades del proyecto

def lista_reportes(request): # Lista todos los reportes
    return HttpResponse('Listado de reportes (placeholder)') # Responde con texto plano

def crear_reporte(request): # Crea un nuevo reporte
    return HttpResponse('Crear reporte (placeholder)') # Responde con texto plano

def detalle_reporte(request, reporte_id): # Muestra los detalles de un reporte
    return HttpResponse(f'Detalle reporte {reporte_id} (placeholder)') # Responde con texto plano

def editar_reporte(request, reporte_id): # Edita un reporte
    return HttpResponse(f'Editar reporte {reporte_id} (placeholder)') # Responde con texto plano

def eliminar_reporte(request, reporte_id): # Elimina un reporte
    return HttpResponse(f'Eliminar reporte {reporte_id} (placeholder)') # Responde con texto plano
