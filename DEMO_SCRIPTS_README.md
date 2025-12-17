# 🧪 Scripts de Demostración - Sistema Neonatal

Este directorio contiene dos scripts para demostrar el funcionamiento del Sistema Neonatal ante clientes finales.

## 📋 Scripts Disponibles

### 1. **`test_demo.sh`** - Demo Completa (Recomendado)

Script completo que ejecuta todas las pruebas del sistema.

**Uso:**
```bash
./test_demo.sh
```

**Qué prueba:**
- ✓ Entorno virtual y dependencias
- ✓ Conectividad con MySQL
- ✓ Usuarios en la base de datos
- ✓ Login de 5 usuarios diferentes
- ✓ API del dashboard del supervisor
- ✓ Acceso a reportes REM A24
- ✓ Exportación a Excel/PDF
- ✓ Sistema de backups automáticos
- ✓ Estado de servicios (MySQL, Nginx, Gunicorn, SAMBA)

**Duración:** ~30 segundos  
**Output:** Detallado con colores e iconos

---

### 2. **`demo_quick.sh`** - Demo Rápida

Script simplificado para demostración rápida (ideal para presentaciones cortas).

**Uso:**
```bash
./demo_quick.sh
```

**Qué prueba:**
- ✓ Base de datos operativa
- ✓ Login de 3 usuarios clave
- ✓ API del dashboard
- ✓ Reportes y exportaciones

**Duración:** ~10 segundos  
**Output:** Compacto y visual

---

## 🎯 Guía de Uso por Escenario

### Escenario 1: Presentación Ejecutiva (5-10 min)
```bash
./demo_quick.sh
# Luego acceder a http://sistema.neonatal con supervisor1/Inacap2025*
```

### Escenario 2: Demo Técnica Completa (15-20 min)
```bash
./test_demo.sh
# Muestra todas las características y verificaciones
```

### Escenario 3: Verificación Rápida (Mantenimiento)
```bash
./demo_quick.sh
# Confirmar que todo está funcionando
```

---

## 👤 Credenciales para Demostración

**Usuario:** `supervisor1`  
**Contraseña:** `Inacap2025*`

Otros usuarios disponibles:
- `admin1` (ADMIN)
- `matrona1` (MATRONA)
- `auditor1` (AUDITORIA)
- `exempleado` (SOME)

---

## 🌐 Acceso Web

**URL:** `http://sistema.neonatal` o `http://localhost`

Desde la red local, cualquier PC puede acceder a:
```
http://10.155.12.62
```

(Ajusta la IP según tu red)

---

## 📊 Funcionalidades que Puedes Demostrar

### 1. **Dashboard Supervisor**
- Estadísticas en tiempo real
- Gráficos interactivos
- Distribución de reportes por tipo

### 2. **Reportes REM A24**
- Visualización de datos filtrados
- Exportación a Excel (.xlsx)
- Exportación a PDF
- Filtro por mes y año

### 3. **Sistema de Backups**
- Acceso desde múltiples equipos (Windows, Mac, Linux)
- Compartición SAMBA automática
- Ejecución diaria a las 2 AM
- Retención automática de 30 días

### 4. **Gestión de Usuarios**
- Panel de administración
- Creación/edición de usuarios
- Asignación de roles
- Auditoría de cambios

---

## 🔍 Interpretación de Resultados

### ✓ EXITOSO
Todo está funcionando correctamente. El sistema está listo para usar.

### ✗ FALLÓ
Hay un problema. Verifica los logs:
```bash
# Para problemas de Base de Datos
systemctl status mysql
journalctl -u mysql -n 20

# Para problemas de Aplicación
journalctl -u gunicorn-neonatal -n 50

# Para problemas de Servicio Web
systemctl status nginx
```

---

## 📝 Personalización

### Cambiar horario de backup
Edita el archivo `/etc/cron.d/neonatal-backup` o usa:
```bash
crontab -e
```

### Cambiar usuario demo
Modifica las credenciales en `neonatal/settings.py` o crea nuevos usuarios con:
```bash
python manage.py createsuperuser
```

### Cambiar IP/Host
En `neonatal/settings.py`:
```python
ALLOWED_HOSTS = ['*', 'tu-host-aqui', '10.x.x.x']
```

---

## 🛠️ Solución de Problemas

### "Entorno virtual no encontrado"
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### "MySQL: Connection refused"
```bash
systemctl status mysql
systemctl restart mysql
```

### "Nginx: 404 Not Found"
```bash
sudo systemctl status nginx
sudo nginx -t
```

### "Permiso denegado" al ejecutar scripts
```bash
chmod +x test_demo.sh
chmod +x demo_quick.sh
```

---

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

**Sistema:** Neonatal v1.0  
**Última actualización:** 17 de Diciembre de 2025  
**Estado:** ✅ Producción
