
# pylint: disable=no-member
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Auditoria

# ===============================
# Auditoría: solo visualización
# ===============================
# Solo usuarios autenticados y con rol AUDITORIA pueden ver los logs.
@login_required
def lista_auditorias(request):
    """
    Lista todos los registros de auditoría.
    Acceso exclusivo para usuarios con rol 'AUDITORIA'.
    """
    if getattr(request.user, 'role', None) != 'AUDITORIA':
        return HttpResponseForbidden('Algo salio mal.')
    logs = Auditoria.objects.all()
    return render(request, 'auditoria/lista_auditorias.html', {'logs': logs})

@login_required
def detalle_auditoria(request, auditoria_id):
    """
    Muestra el detalle de un registro de auditoría.
    Acceso exclusivo para usuarios con rol 'AUDITORIA'.
    """
    if getattr(request.user, 'role', None) != 'AUDITORIA':
        return HttpResponseForbidden('Algo salio mal.')
    try:
        log = Auditoria.objects.get(pk=auditoria_id)
    except Auditoria.DoesNotExist:
        return HttpResponse('Registro de auditoría no encontrado.', status=404)
    return render(request, 'auditoria/detalle_auditoria.html', {'log': log})

# Nota: No existen vistas para crear, editar ni eliminar logs de auditoría.
# El registro es automático y la auditoría es solo de consulta.

# ===============================
# Vista temporal para crear auditoría manualmente
# ===============================

# ===============================
# Vista temporal para crear auditoría manualmente
# ===============================
#
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect
#
# @csrf_exempt
# @login_required
# def crear_auditoria(request):
#     """
#     Vista temporal para crear un registro de auditoría desde un formulario simple.
#     Solo para pruebas. Usar SOLO si makemigrations/migrate no crea la tabla correctamente.
#     Comentar o eliminar después de poblar la base de datos.
#     """
#     if request.method == 'POST':
#         usuario = request.user
#         accion_realizada = request.POST.get('accion_realizada', 'PRUEBA')
#         modelo_afectado = request.POST.get('modelo_afectado', 'TestModel')
#         registro_id = request.POST.get('registro_id', 1)
#         detalles_cambio = request.POST.get('detalles_cambio', 'Detalle de prueba')
#         ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
#         Auditoria.objects.create(
#             usuario=usuario,
#             accion_realizada=accion_realizada,
#             modelo_afectado=modelo_afectado,
#             registro_id=registro_id,
#             detalles_cambio=detalles_cambio,
#             ip_address=ip_address
#         )
#         return redirect('lista_auditorias')
#     return render(request, 'auditoria/crear_auditoria.html')
