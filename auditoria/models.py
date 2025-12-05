# pylint: disable=no-member
def registrar_evento_auditoria(
	usuario=None,
	accion_realizada=None,
	modelo_afectado=None,
	registro_id=None,
	detalles_cambio=None,
	ip_address=None
):
	"""
	Helper para registrar un evento de auditoría desde cualquier vista o señal.
	Ejemplo de uso:
		registrar_evento_auditoria(
			usuario=request.user,
			accion_realizada='CREATE',
			modelo_afectado='Madre',
			registro_id=madre.id,
			detalles_cambio='Se creó un nuevo registro de madre',
			ip_address=request.META.get('REMOTE_ADDR')
		)
	"""
	from .models import Auditoria
	Auditoria.objects.create(
		usuario=usuario if usuario and usuario.is_authenticated else None,
		accion_realizada=accion_realizada,
		modelo_afectado=modelo_afectado,
		registro_id=registro_id,
		detalles_cambio=detalles_cambio,
		ip_address=ip_address
	)
from django.db import models
from django.conf import settings

class Auditoria(models.Model):
	usuario = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		verbose_name="Usuario Involucrado"
	)
	fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora del Evento")
	ACCIONES_CHOICES = [
		('CREATE', 'Creación de Registro'),
		('UPDATE', 'Actualización de Registro'),
		('DELETE', 'Eliminación de Registro'),
		('LOGIN_SUCCESS', 'Inicio de Sesión Exitoso'),
		('LOGIN_FAILED', 'Intento de Inicio de Sesión Fallido'),
		('LOGOUT', 'Cierre de Sesión'),
		('ACCESS_DENIED', 'Intento de Acceso No Autorizado'),
		('USER_BLOCKED', 'Usuario Bloqueado por Seguridad'),
		('TOKEN_RECOVERY', 'Uso de Enlace de Recuperación de Contraseña')
	]
	accion_realizada = models.CharField(max_length=50, choices=ACCIONES_CHOICES, verbose_name="Tipo de Evento Registrado")
	modelo_afectado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modelo Afectado (Ej: 'Parto', 'Usuario')")
	registro_id = models.IntegerField(blank=True, null=True, verbose_name="ID del Registro Afectado")
	detalles_cambio = models.TextField(blank=True, null=True, verbose_name="Detalles, Datos 'Antes' y 'Después', o Mensaje de Error")
	ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP del Cliente")

	class Meta:
		verbose_name = "Registro de Trazabilidad y Auditoría"
		verbose_name_plural = "Registros de Trazabilidad y Auditoría"
		ordering = ['-fecha_hora']

	def __str__(self):
		return f"[{self.fecha_hora.strftime('%Y-%m-%d %H:%M')}] {self.accion_realizada} | Modelo: {self.modelo_afectado} ID: {self.registro_id}"
from django.db import models # Sistema de modelos de Django
