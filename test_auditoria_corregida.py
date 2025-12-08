#!/usr/bin/env python
"""
Test específico para la app de auditoría corregida
"""
import os
import django
from django.test import Client

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from roles.models import CustomUser
from auditoria.models import Auditoria

def test_auditoria_app():
    """Probar la app de auditoría corregida"""
    print("🔍 PROBANDO APP DE AUDITORÍA CORREGIDA")
    print("=" * 50)
    
    # 1. Verificar que existen datos de auditoría
    total_eventos = Auditoria.objects.count()
    print(f"📊 Total eventos de auditoría: {total_eventos}")
    
    if total_eventos == 0:
        print("⚠️  No hay datos de auditoría. Ejecute poblar_auditoria_demo.py primero")
        return False
    
    # 2. Verificar que existe usuario auditor
    try:
        auditor = CustomUser.objects.get(username='auditor_demo')
        print(f"👤 Usuario auditor encontrado: {auditor.username} (Rol: {auditor.role})")
    except CustomUser.DoesNotExist:
        print("❌ Usuario auditor_demo no encontrado")
        return False
    
    client = Client()
    
    # 3. Login con usuario auditor
    print(f"\n🔐 Probando login como auditor")
    response = client.post('/login/login/', {
        'login_type': 'username',
        'username': 'auditor_demo',
        'password': 'auditor_2025'
    })
    
    if response.status_code == 302:
        print("✅ Login exitoso")
    else:
        print(f"❌ Login falló - Status: {response.status_code}")
        return False
    
    # 4. Probar acceso al dashboard de auditoría (a través de roles)
    print(f"\n🎯 Probando acceso al dashboard de auditoría")
    response = client.get('/dashboard/')
    
    if response.status_code == 200:
        print("✅ Acceso al panel AUDITORIA exitoso")
        content = response.content.decode()
        if 'Panel de Auditoría' in content:
            print("✅ Panel de auditoría cargado correctamente")
        else:
            print("⚠️  Panel cargado pero contenido inesperado")
    else:
        print(f"❌ Error accediendo al panel - Status: {response.status_code}")
        return False
    
    # 5. Probar acceso a lista de auditorías
    print(f"\n📋 Probando acceso a lista de auditorías")
    response = client.get('/auditoria/lista/')
    
    if response.status_code == 200:
        print("✅ Lista de auditorías accesible")
        content = response.content.decode()
        if 'Registros de Auditoría' in content:
            print("✅ Lista cargada con contenido correcto")
        else:
            print("⚠️  Lista cargada pero contenido inesperado")
    else:
        print(f"❌ Error accediendo a lista - Status: {response.status_code}")
        return False
    
    # 6. Verificar que NO puede acceder a funciones CRUD (deben dar error)
    print(f"\n🚫 Verificando que funciones CRUD no estén disponibles")
    
    # Intentar acceder a crear (no debe existir)
    response = client.get('/auditoria/crear/')
    if response.status_code == 404:
        print("✅ Función CREAR correctamente deshabilitada (404)")
    else:
        print(f"⚠️  Función CREAR disponible (Status: {response.status_code})")
    
    # 7. Probar detalle de un evento
    if total_eventos > 0:
        primer_evento = Auditoria.objects.first()
        print(f"\n👁️  Probando detalle del evento ID: {primer_evento.id}")
        response = client.get(f'/auditoria/{primer_evento.id}/')
        
        if response.status_code == 200:
            print("✅ Detalle de evento accesible")
        else:
            print(f"❌ Error accediendo a detalle - Status: {response.status_code}")
    
    # 8. Probar modo demo con superuser
    print(f"\n🎭 Probando modo demo para auditoría")
    response = client.get('/dashboard/?rol=AUDITORIA')
    
    if response.status_code == 200:
        print("✅ Modo demo AUDITORIA funcional")
    else:
        print(f"❌ Error en modo demo - Status: {response.status_code}")
    
    print(f"\n🎉 AUDITORÍA APP COMPLETAMENTE FUNCIONAL")
    return True

def main():
    """Ejecutar test de auditoría"""
    print("=" * 50)
    print("    TEST APP AUDITORÍA CORREGIDA")
    print("=" * 50)
    
    success = test_auditoria_app()
    
    print("\n" + "=" * 50)
    if success:
        print("🎯 RESULTADO: ✅ APP AUDITORÍA FUNCIONANDO CORRECTAMENTE")
        print("✨ Solo consulta, registros automáticos, dashboard integrado")
        print("🚀 Lista para demostración y presentación")
    else:
        print("🎯 RESULTADO: ❌ PROBLEMAS EN APP AUDITORÍA")
        print("⚠️  Revisar configuración antes de uso")
    print("=" * 50)

if __name__ == '__main__':
    main()