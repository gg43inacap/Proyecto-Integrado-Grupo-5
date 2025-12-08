#!/usr/bin/env python
"""
Script para poblar datos de auditoría de demostración
Los registros se crean usando la función automática del sistema
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from django.contrib.auth import get_user_model
from auditoria.models import registrar_evento_auditoria
import random
from datetime import datetime, timedelta

def poblar_auditoria_demo():
    """Crear datos de auditoría de demostración usando el sistema automático"""
    print("🎭 POBLANDO DATOS DE AUDITORÍA PARA DEMOSTRACIÓN")
    print("=" * 60)
    
    User = get_user_model()
    usuarios = list(User.objects.all())
    
    if not usuarios:
        print("❌ No hay usuarios en el sistema. Cree usuarios primero.")
        return False
    
    # Datos de ejemplo realistas
    acciones = ['CREATE', 'UPDATE', 'DELETE', 'VIEW', 'LOGIN', 'LOGOUT']
    modelos = ['Madre', 'Parto', 'RN', 'Usuario', 'Auditoria']
    
    eventos_creados = 0
    
    print(f"👥 Usuarios disponibles: {len(usuarios)}")
    print(f"🎯 Creando eventos de auditoría...")
    
    for i in range(25):  # Crear 25 eventos de ejemplo
        try:
            usuario = random.choice(usuarios)
            accion = random.choice(acciones)
            modelo = random.choice(modelos)
            registro_id = random.randint(1, 100)
            
            # Generar detalles realistas según la acción
            detalles = generar_detalle_realista(accion, modelo, registro_id)
            
            # IPs de ejemplo
            ips_ejemplo = ['127.0.0.1', '192.168.1.10', '192.168.1.25', '10.0.0.5', '172.16.0.10']
            ip = random.choice(ips_ejemplo)
            
            # Usar la función automática del sistema
            registrar_evento_auditoria(
                usuario=usuario,
                accion_realizada=accion,
                modelo_afectado=modelo,
                registro_id=registro_id,
                detalles_cambio=detalles,
                ip_address=ip
            )
            
            eventos_creados += 1
            print(f"   ✅ {eventos_creados}/25: {usuario.username} -> {accion} en {modelo}")
            
        except Exception as e:
            print(f"   ❌ Error creando evento {i+1}: {e}")
    
    print(f"\n🎉 COMPLETADO: {eventos_creados} eventos de auditoría creados")
    print("✨ Los datos están listos para demostración")
    return True

def generar_detalle_realista(accion, modelo, registro_id):
    """Generar detalles realistas para los eventos"""
    detalles_templates = {
        'CREATE': {
            'Madre': f'Nueva madre registrada en el sistema con ID #{registro_id}. Datos: nombre, RUT, fecha nacimiento completados.',
            'Parto': f'Nuevo parto registrado con ID #{registro_id}. Vinculado a madre, fecha y tipo de parto especificados.',
            'RN': f'Recién nacido registrado con ID #{registro_id}. Datos completos: peso, talla, APGAR, vinculado a parto.',
            'Usuario': f'Nuevo usuario creado con ID #{registro_id}. Rol asignado y credenciales configuradas.',
            'Auditoria': f'Registro de auditoría #{registro_id} creado automáticamente por el sistema.'
        },
        'UPDATE': {
            'Madre': f'Información de madre ID #{registro_id} actualizada. Campos modificados: dirección, teléfono, antecedentes.',
            'Parto': f'Datos del parto ID #{registro_id} actualizados. Estado cambiado a completado.',
            'RN': f'Información del RN ID #{registro_id} modificada. Actualización de datos clínicos.',
            'Usuario': f'Usuario ID #{registro_id} modificado. Cambios en rol o información personal.',
            'Auditoria': f'Registro de auditoría #{registro_id} consultado para revisión.'
        },
        'DELETE': {
            'Madre': f'Madre ID #{registro_id} eliminada del sistema tras validación de procedimientos.',
            'Parto': f'Registro de parto ID #{registro_id} eliminado por corrección de datos.',
            'RN': f'Registro de RN ID #{registro_id} eliminado tras revisión médica.',
            'Usuario': f'Usuario ID #{registro_id} eliminado del sistema por solicitud administrativa.',
            'Auditoria': f'Acceso denegado para eliminar registro de auditoría #{registro_id}.'
        },
        'VIEW': {
            'Madre': f'Consulta realizada en listado de madres. Registro ID #{registro_id} visualizado.',
            'Parto': f'Lista de partos consultada. Detalles del parto ID #{registro_id} revisados.',
            'RN': f'Información del RN ID #{registro_id} consultada para seguimiento.',
            'Usuario': f'Lista de usuarios accedida. Usuario ID #{registro_id} consultado.',
            'Auditoria': f'Eventos de auditoría consultados. Registro ID #{registro_id} revisado.'
        },
        'LOGIN': {
            'Madre': f'Acceso al módulo de gestión de madres. Sesión iniciada correctamente.',
            'Parto': f'Usuario accedió al sistema de registro de partos desde panel.',
            'RN': f'Ingreso al módulo de recién nacidos. Autenticación exitosa.',
            'Usuario': f'Login exitoso en panel de administración de usuarios.',
            'Auditoria': f'Acceso al sistema de auditoría. Sesión de consulta iniciada.'
        },
        'LOGOUT': {
            'Madre': f'Sesión cerrada desde módulo de madres. Logout seguro completado.',
            'Parto': f'Usuario cerró sesión desde sistema de partos. Fin de sesión registrado.',
            'RN': f'Logout desde módulo RN. Sesión terminada correctamente.',
            'Usuario': f'Cierre de sesión desde administración. Logout seguro.',
            'Auditoria': f'Sesión de auditoría finalizada. Logout del sistema de monitoreo.'
        }
    }
    
    return detalles_templates.get(accion, {}).get(modelo, f'{accion} realizada en {modelo} ID #{registro_id}')

if __name__ == '__main__':
    poblar_auditoria_demo()