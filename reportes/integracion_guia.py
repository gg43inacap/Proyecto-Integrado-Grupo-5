"""
GUÍA DE INTEGRACIÓN - APP REPORTES
==================================

Esta guía ayuda a integrar completamente la app de reportes cuando esté lista.

🎯 ESTADO ACTUAL:
- ✅ App 'reportes' ya está en INSTALLED_APPS
- ✅ URLs básicas ya configuradas
- ✅ Tests preparatorios creados
- ✅ Estructura base lista
- ⏳ Pendiente: Vistas funcionales y templates

📋 CHECKLIST DE INTEGRACIÓN:
"""

# ============================================================================
# 1. MODELOS DE REPORTES (reportes/models.py)
# ============================================================================

class ReporteIntegracion:
    """
    Modelo sugerido para reportes que se integra con auditoría:
    
    from django.db import models
    from django.conf import settings
    from auditoria.models import registrar_evento_auditoria
    
    class Reporte(models.Model):
        TIPOS_REPORTE = [
            ('PARTOS_MENSUAL', 'Reporte Mensual de Partos'),
            ('RN_ESTADISTICAS', 'Estadísticas de Recién Nacidos'),
            ('MADRES_SEGUIMIENTO', 'Seguimiento de Madres'),
            ('AUDITORIA_SISTEMA', 'Reporte de Auditoría'),
        ]
        
        nombre = models.CharField(max_length=200)
        tipo_reporte = models.CharField(max_length=50, choices=TIPOS_REPORTE)
        fecha_generacion = models.DateTimeField(auto_now_add=True)
        generado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        archivo_excel = models.FileField(upload_to='reportes/', blank=True)
        parametros_filtros = models.JSONField(default=dict)  # Para filtros aplicados
        
        def save(self, *args, **kwargs):
            is_new = self.pk is None
            super().save(*args, **kwargs)
            
            if is_new:
                registrar_evento_auditoria(
                    usuario=self.generado_por,
                    accion_realizada='CREATE',
                    modelo_afectado='Reporte',
                    registro_id=self.id,
                    detalles_cambio=f'Reporte generado: {self.nombre} - {self.get_tipo_reporte_display()}'
                )
    """

# ============================================================================
# 2. VISTAS CON AUDITORÍA (reportes/views.py)
# ============================================================================

class VistasIntegracion:
    """
    Ejemplo de vista que integra con auditoría:
    
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import render, redirect
    from auditoria.models import registrar_evento_auditoria
    from gestion_some.models import Madre
    from partos.models import Parto, RN
    import pandas as pd
    import io
    from django.http import HttpResponse
    
    @login_required
    def generar_reporte_partos(request):
        # Verificar permisos (ADMIN, SUPERVISOR)
        if request.user.role not in ['ADMIN', 'SUPERVISOR']:
            return HttpResponseForbidden()
            
        if request.method == 'POST':
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            
            # Generar reporte
            partos = Parto.objects.filter(
                fecha_hora__date__range=[fecha_inicio, fecha_fin]
            ).select_related('madre')
            
            # Crear Excel
            df = pd.DataFrame([{
                'Fecha': parto.fecha_hora,
                'Madre': parto.madre.nombre,
                'RUT': parto.madre.rut,
                'Tipo': parto.get_tipo_parto_display(),
                'Estado': parto.get_estado_display(),
            } for parto in partos])
            
            # Generar archivo Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Partos', index=False)
            
            # Registrar auditoría
            registrar_evento_auditoria(
                usuario=request.user,
                accion_realizada='CREATE',
                modelo_afectado='Reporte',
                detalles_cambio=f'Reporte partos generado: {fecha_inicio} a {fecha_fin}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Respuesta con archivo
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="reporte_partos_{fecha_inicio}_{fecha_fin}.xlsx"'
            return response
            
        return render(request, 'reportes/generar_partos.html')
    """

# ============================================================================
# 3. TEMPLATES DE INTEGRACIÓN
# ============================================================================

class TemplatesIntegracion:
    """
    Templates sugeridos que se integran con el sistema:
    
    reportes/templates/reportes/
    ├── base_reportes.html          # Extiende base.html
    ├── lista_reportes.html         # Lista de reportes disponibles
    ├── generar_partos.html         # Formulario para reporte de partos
    ├── generar_rn.html            # Formulario para reporte de RN
    ├── dashboard_reportes.html     # Dashboard con gráficos
    └── auditoria_reportes.html     # Reporte de auditoría
    
    Ejemplo de base_reportes.html:
    {% extends 'base.html' %}
    {% block title %}Reportes - Sistema Neonatal{% endblock %}
    {% block content %}
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-3">
                <div class="card">
                    <div class="card-header">
                        <h5>Tipos de Reportes</h5>
                    </div>
                    <div class="list-group list-group-flush">
                        <a href="{% url 'reporte_partos' %}" class="list-group-item">
                            📊 Reportes de Partos
                        </a>
                        <a href="{% url 'reporte_rn' %}" class="list-group-item">
                            👶 Reportes RN
                        </a>
                        <a href="{% url 'reporte_madres' %}" class="list-group-item">
                            👩 Seguimiento Madres
                        </a>
                        <a href="{% url 'reporte_auditoria' %}" class="list-group-item">
                            🔍 Auditoría Sistema
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-9">
                {% block reportes_content %}{% endblock %}
            </div>
        </div>
    </div>
    {% endblock %}
    """

# ============================================================================
# 4. ACTUALIZAR PANELES DE ROLES
# ============================================================================

def actualizar_paneles():
    """
    Agregar enlaces a reportes en los paneles:
    
    En roles/templates/roles/panel_ADMIN.html:
    <a href="{% url 'reportes_dashboard' %}" class="btn btn-info">
        <i class="fas fa-chart-bar"></i> Ver Reportes
    </a>
    
    En roles/templates/roles/panel_SUPERVISOR.html:
    <a href="{% url 'reportes_dashboard' %}" class="btn btn-info">
        <i class="fas fa-chart-bar"></i> Reportes y Estadísticas
    </a>
    """

# ============================================================================
# 5. DEPENDENCIAS NECESARIAS
# ============================================================================

DEPENDENCIAS = """
# Agregar a requirements.txt:
pandas>=1.5.0
openpyxl>=3.0.0
matplotlib>=3.6.0
plotly>=5.0.0
"""

# ============================================================================
# 6. TESTS DE INTEGRACIÓN
# ============================================================================

class TestsIntegracion:
    """
    Tests que ya están preparados en reportes/tests.py
    
    Agregar estos tests cuando las vistas estén listas:
    
    def test_generar_reporte_registra_auditoria(self):
        response = self.client.post('/reportes/generar-partos/', {
            'fecha_inicio': '2025-01-01',
            'fecha_fin': '2025-12-31'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Auditoria.objects.filter(
                modelo_afectado='Reporte',
                accion_realizada='CREATE'
            ).exists()
        )
    """

# ============================================================================
# 7. COMANDOS PARA INTEGRACIÓN
# ============================================================================

COMANDOS_INTEGRACION = """
# 1. Instalar dependencias
pip install pandas openpyxl matplotlib plotly

# 2. Hacer migraciones si hay modelos nuevos
python manage.py makemigrations reportes
python manage.py migrate

# 3. Ejecutar tests
python manage.py test reportes.tests

# 4. Verificar integración completa
python test_esenciales.py

# 5. Verificar que URLs funcionen
python manage.py check --deploy
"""

if __name__ == '__main__':
    print("📋 GUÍA DE INTEGRACIÓN APP REPORTES")
    print("=" * 50)
    print("✅ URLs configuradas")
    print("✅ Tests preparados") 
    print("✅ Estructura lista")
    print("⏳ Pendiente: Implementación de vistas y templates")
    print("\n💡 Ver este archivo para guía completa de integración")