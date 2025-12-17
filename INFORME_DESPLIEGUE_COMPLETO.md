# 📋 INFORME TÉCNICO COMPLETO - DESPLIEGUE DJANGO NEONATAL EN LAN

**Fecha**: 17 de diciembre de 2025  
**Proyecto**: Sistema de Gestión Neonatal  
**Versión Django**: 5.2.8  
**Base de Datos**: MySQL 8.0.44  
**Servidor Web**: Nginx 1.24.0  
**App Server**: Gunicorn 23.0.0

---

## 📍 ÍNDICE DE CONTENIDOS

1. [Descripción General](#descripción-general)
2. [Estructura de Directorios](#estructura-de-directorios)
3. [Orden de Ejecución de Programas](#orden-de-ejecución-de-programas)
4. [Ubicación de Archivos Clave](#ubicación-de-archivos-clave)
5. [Cómo Funciona Cada Componente](#cómo-funciona-cada-componente)
6. [Credenciales y Acceso](#credenciales-y-acceso)
7. [Comandos Frecuentes](#comandos-frecuentes)

---

## 🎯 DESCRIPCIÓN GENERAL

Este es un despliegue de una aplicación Django para gestión hospitalaria neonatal en una red local (LAN). La arquitectura implementada es **producción-like** usando:

- **Frontend**: Bootstrap + HTML/CSS/JavaScript (servidos por Nginx)
- **Backend**: Django 5.2.8 (ejecutado con Gunicorn)
- **Base de Datos**: MySQL 8.0.44
- **Servidor Web**: Nginx (proxy inverso + servidor estático)
- **Respaldo**: Samba/SMB para NAS

**Acceso**:
- Máquina local: `http://127.0.0.1/`
- Red LAN: `http://sistema.neonatal/` (dominio local)
- IP del servidor: `10.155.12.62` (Este puede variar, se debe verificar con el comando "hostname -I" en la terminal de Linux Ubuntu)

---

## 📂 ESTRUCTURA DE DIRECTORIOS

```
/home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5/
│
├── .venv/                              # Entorno virtual Python
│   └── bin/
│       ├── python3                     # Python ejecutable
│       └── gunicorn                    # Gunicorn ejecutable
│
├── neonatal/                           # Configuración principal Django
│   ├── settings.py                     # Configuración de Django
│   ├── urls.py                         # Rutas principales
│   ├── wsgi.py                         # Interfaz WSGI
│   └── views.py                        # Vistas del proyecto
│
├── roles/                              # App: Gestión de roles y usuarios
│   ├── models.py                       # Modelo CustomUser
│   ├── views.py                        # Lógica de dashboards
│   ├── urls.py                         # Rutas de roles
│   └── templates/roles/                # Templates por rol
│       ├── panel_admin.html
│       ├── panel_some.html
│       ├── panel_matrona.html
│       ├── panel_supervisor.html
│       └── panel_auditoria.html
│
├── login/                              # App: Autenticación
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/login/
│
├── partos/                             # App: Registro de partos
│   ├── models.py                       # Modelo Parto, RN
│   ├── views.py
│   ├── urls.py
│   └── templates/partos/
│
├── gestion_some/                       # App: Gestión de madres SOME
│   ├── models.py                       # Modelo Madre
│   ├── views.py
│   ├── urls.py
│   └── templates/gestion_some/
│
├── auditoria/                          # App: Auditoría
│   ├── models.py                       # Modelo Auditoria
│   ├── views.py
│   ├── urls.py
│   └── templates/auditoria/
│
├── reportes/                           # App: Generación de reportes
│   ├── models.py                       # Modelo Reporte
│   ├── views.py
│   ├── urls.py
│   └── templates/reportes/
│
├── templates/                          # Templates globales
│   ├── base.html                       # Plantilla base
│   ├── inicio.html                     # Página principal
│   ├── 404.html                        # Error 404
│   └── 500.html                        # Error 500
│
├── static/                             # Archivos estáticos (desarrollo)
│   ├── css/
│   │   ├── base/
│   │   │   ├── variables.css
│   │   │   └── base.css
│   │   └── apps/
│   │       ├── inicio.css
│   │       ├── login.css
│   │       ├── crear_parto.css
│   │       └── ... (16 archivos CSS)
│   ├── js/
│   │   ├── datepicker.js
│   │   ├── verificar_rut.js
│   │   ├── rut_format.js
│   │   ├── inicio.js
│   │   └── ... (20+ archivos JS)
│   └── images/
│       └── logoHospital.png
│
├── staticfiles/                        # Archivos estáticos compilados (producción)
│   ├── css/                            # CSS servidos por Nginx
│   ├── js/                             # JavaScript servidos por Nginx
│   └── images/                         # Imágenes servidas por Nginx
│
├── manage.py                           # Script de administración Django
├── requirements.txt                    # Dependencias Python
├── .env                                # Variables de entorno
├── README.md                           # Documentación
├── BACKUP_CONFIG.md                    # Documentación de backups
│
└── /home/hospital/                     # Directorio del usuario
    ├── backup-mysql.sh                 # Script de backup automático
    ├── neonatal-backups/               # Carpeta de backups
    └── Escritorio/
        ├── Base-Datos-Neonatal.desktop # Atajo a DB
        ├── abrir-mysql-cli.sh          # Cliente MySQL
        ├── DB-Browser.desktop          # Gestor de BD visual
        └── MySQL-Neonatal.desktop      # Atajo alternativo a DB
```

---

## ⏱️ ORDEN DE EJECUCIÓN DE PROGRAMAS (Al encender la máquina)

### **PASO 1: Activar el Entorno Virtual Python** ⚙️
```bash
cd /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5
source .venv/bin/activate
```
**Qué hace**: Carga todas las dependencias Python necesarias (Django, Gunicorn, MySQL, etc.)  
**Dónde**: `.venv/bin/activate`

---

### **PASO 2: Iniciar MySQL** 🗄️
```bash
sudo systemctl start mysql
# O verificar estado:
sudo systemctl status mysql
```
**Qué hace**: Inicia el servidor de base de datos en puerto 3306  
**Ubicación del servicio**: `/etc/mysql/` (configuración)  
**Archivos de datos**: `/var/lib/mysql/neonatal/` (donde están las tablas .ibd)

---

### **PASO 3: Iniciar Gunicorn (App Server)** 🚀
```bash
sudo systemctl start gunicorn-neonatal
# Verificar:
sudo systemctl status gunicorn-neonatal
```
**Qué hace**: Ejecuta la aplicación Django con 3 workers  
**Ubicación del servicio**: `/etc/systemd/system/gunicorn-neonatal.service`  
**Socket Unix**: `/run/gunicorn/neonatal.sock`  
**Archivos de configuración**:
- Script: `/home/hospital/backup-mysql.sh`
- Comando: `gunicorn --workers 3 --bind unix:/run/gunicorn/neonatal.sock neonatal.wsgi:application`

---

### **PASO 4: Iniciar Nginx (Servidor Web)** 🌐
```bash
sudo systemctl start nginx
# Verificar:
sudo systemctl status nginx
```
**Qué hace**: Sirve archivos estáticos, proxy a Gunicorn, escucha puerto 80  
**Ubicación del config**: `/etc/nginx/sites-available/neonatal`  
**Archivo de log**: `/var/log/nginx/error.log` (errores) y `/var/log/nginx/access.log` (accesos)

---

### **PASO 5: Iniciar Samba (Compartir archivos)** 📂
```bash
sudo systemctl start smbd nmbd
# Verificar:
sudo systemctl status smbd nmbd
```
**Qué hace**: Permite que el NAS acceda a MySQL y backups vía SMB/CIFS  
**Ubicación del config**: `/etc/samba/smb.conf`  
**Compartidos**:
- `mysql-data`: `/var/lib/mysql/` (datos en vivo)
- `neonatal-backups`: `/home/hospital/neonatal-backups/` (respaldos)

---

### **PASO 6: Verificar que todo esté corriendo** ✅
```bash
sudo systemctl status nginx gunicorn-neonatal mysql smbd nmbd
```

**Resultado esperado**: Todos los servicios muestran `active (running)`

---

## 📍 UBICACIÓN DE ARCHIVOS CLAVE

### **Configuración de Django**
| Archivo | Ubicación | Qué hace |
|---------|-----------|----------|
| settings.py | `neonatal/settings.py` | Configuración principal (BD, ALLOWED_HOSTS, STATIC_ROOT) |
| urls.py | `neonatal/urls.py` | Enrutamiento de URLs (ruta admin en `/sistema-admin-hospitalario/`) |
| wsgi.py | `neonatal/wsgi.py` | Interfaz para Gunicorn |
| manage.py | Raíz del proyecto | Script para comandos de administración |
| requirements.txt | Raíz del proyecto | Lista de dependencias Python |
| .env | Raíz del proyecto | Variables de entorno (`DATABASE_URL=mysql://...`) |

### **Base de Datos**
| Elemento | Ubicación |
|----------|-----------|
| Datos MySQL | `/var/lib/mysql/neonatal/` |
| Tablas (.ibd) | `/var/lib/mysql/neonatal/` (15 tablas) |
| Backups | `/home/hospital/neonatal-backups/` |
| Script backup | `/home/hospital/backup-mysql.sh` |

### **Servicios del Sistema**
| Servicio | Archivo de configuración |
|----------|--------------------------|
| Gunicorn | `/etc/systemd/system/gunicorn-neonatal.service` |
| Nginx | `/etc/nginx/sites-available/neonatal` |
| Samba | `/etc/samba/smb.conf` |
| Cron (backups) | `sudo crontab -l` |
| Hosts locales | `/etc/hosts` (contiene `127.0.0.1 sistema.neonatal`) |

### **Archivos de Log**
| Servicio | Log |
|----------|-----|
| Nginx | `/var/log/nginx/error.log` y `/var/log/nginx/access.log` |
| Gunicorn | `sudo journalctl -u gunicorn-neonatal` |
| MySQL | `/var/log/mysql/error.log` |
| Backups | `/var/log/neonatal-backup.log` |

---

## 🔧 CÓMO FUNCIONA CADA COMPONENTE

### **1. DJANGO (Backend)**

**Ubicación**: `neonatal/` (carpeta raíz del proyecto)

**Función**: 
- Procesa solicitudes HTTP
- Gestiona la lógica de negocio
- Autentica usuarios
- Interactúa con la BD

**Flujo**:
1. Usuario solicita `http://sistema.neonatal/`
2. Nginx recibe la solicitud
3. Nginx la envía a Gunicorn vía socket Unix
4. Gunicorn ejecuta Django (neonatal.wsgi:application)
5. Django procesa la solicitud según `urls.py`
6. Django renderiza templates y devuelve HTML

**Archivos importantes**:
- `settings.py`: Configuración (BD, apps, static files, etc.)
- `urls.py`: Rutas (`/`, `/login/`, `/roles/dashboard/`, `/sistema-admin-hospitalario/`)
- `roles/views.py`: Lógica de autenticación y dashboards por rol

---

### **2. GUNICORN (Application Server)**

**Ubicación**: `/usr/local/bin/gunicorn` (ejecutable)  
**Configuración**: `/etc/systemd/system/gunicorn-neonatal.service`

**Función**:
- Ejecuta la aplicación Django
- Gestiona múltiples workers (3 procesos simultáneos)
- Comunica con Nginx a través de socket Unix

**Configuración**:
```ini
ExecStart=/home/hospital/.../gunicorn \
  --access-logfile - \
  --workers 3 \
  --bind unix:/run/gunicorn/neonatal.sock \
  neonatal.wsgi:application
```

**Qué significa**:
- `--workers 3`: 3 procesos paralelos (maneja 3 requests simultáneos)
- `--bind unix:...`: Escucha en socket Unix (más rápido que TCP)
- `neonatal.wsgi:application`: Punto de entrada de Django

---

### **3. NGINX (Web Server / Reverse Proxy)**

**Ubicación**: `/etc/nginx/sites-available/neonatal`  
**Ejecutable**: `/usr/sbin/nginx`

**Función**:
- Escucha puerto 80 (HTTP)
- Sirve archivos estáticos directamente (CSS, JS, imágenes)
- Proxy inverso: reenvía requests dinámicas a Gunicorn

**Configuración**:
```nginx
location /static/ {
    alias /home/hospital/.../staticfiles/;  # Sirve estáticos
    expires 30d;
}

location / {
    proxy_pass http://unix:/run/gunicorn/neonatal.sock;  # Django
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

**Ventajas**:
- Estáticos muy rápidos (no pasan por Django)
- Balanceo de carga (podría redirigir a múltiples Gunicorn)
- Seguridad (oculta detalles de Django)

---

### **4. MYSQL (Base de Datos)**

**Ubicación**: `/var/lib/mysql/neonatal/`  
**Puerto**: 3306  
**Versión**: 8.0.44

**Función**:
- Almacena datos de madres, partos, RN, usuarios, auditoría, etc.
- Consultas desde Django

**Tablas principales** (15 total):
- `roles_customuser`: Usuarios del sistema
- `gestion_some_madre`: Datos de madres
- `partos_parto`: Registros de partos
- `partos_rn`: Recién nacidos
- `reportes_reporte`: Reportes generados
- `auditoria_auditoria`: Log de acciones
- `auth_*`: Autenticación Django

**Conexión desde Django**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'hospital',
        'PASSWORD': 'inacap',
        'NAME': 'neonatal',
    }
}
```

---

### **5. SAMBA/SMB (Compartir archivos)**

**Ubicación**: `/etc/samba/smb.conf`

**Función**:
- Permite que dispositivos en la red (NAS) accedan a archivos
- Compartir backups y datos MySQL

**Compartidos**:
```ini
[mysql-data]
path = /var/lib/mysql
valid users = hospital
writable = yes

[neonatal-backups]
path = /home/hospital/neonatal-backups
valid users = hospital
writable = yes
```

**Acceso desde NAS**:
```
smb://10.155.12.62/neonatal-backups
Usuario: hospital
Contraseña: inacap
```

---

### **6. CRON (Backups Automáticos)**

**Ubicación**: `sudo crontab -l`

**Función**:
- Ejecuta script de backup automáticamente cada día a las 2:00 AM

**Configuración**:
```bash
0 2 * * * MYSQL_PASSWORD='inacap' /home/hospital/backup-mysql.sh >> /var/log/neonatal-backup.log 2>&1
```

**Qué hace el script** (`/home/hospital/backup-mysql.sh`):
1. Exporta BD `neonatal` a archivo SQL
2. Comprime con gzip (.sql.gz)
3. Guarda en `/home/hospital/neonatal-backups/`
4. Elimina backups > 30 días
5. Registra en log

**Archivo de backup**: `neonatal_backup_20251217_085913.sql.gz` (4.4 KB)

---

## 🔐 CREDENCIALES Y ACCESO

### **Acceso a la Aplicación Web**

| Usuario | Contraseña | Rol | Acceso |
|---------|-----------|-----|--------|
| admin123 | (su contraseña) | Superadmin Django | `/sistema-admin-hospitalario/` |
| admin1 | (su contraseña) | ADMIN | Dashboard `/roles/dashboard/` |

### **Acceso a Base de Datos**

```
Host: localhost (o 127.0.0.1)
Puerto: 3306
Usuario: hospital
Contraseña: inacap
Base de datos: neonatal
```

### **Acceso Samba/SMB**

```
Ruta: \\10.155.12.62\neonatal-backups
Usuario: hospital
Contraseña: inacap
```

### **SSH (si necesitas acceso remoto)**

```
IP: 10.155.12.62
Puerto: 22
Usuario: hospital
```

---

## 📌 COMANDOS FRECUENTES

### **Gestión de Servicios**

```bash
# Ver estado de todos los servicios
sudo systemctl status nginx gunicorn-neonatal mysql smbd

# Reiniciar un servicio
sudo systemctl restart nginx
sudo systemctl restart gunicorn-neonatal
sudo systemctl restart mysql

# Ver logs en tiempo real
sudo journalctl -u gunicorn-neonatal -f
sudo tail -f /var/log/nginx/error.log
```

### **Django (Management)**

```bash
# Activar entorno virtual
cd /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5
source .venv/bin/activate

# Crear superuser
python manage.py createsuperuser

# Migraciones
python manage.py migrate
python manage.py makemigrations

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear usuario con shell interactivo
python manage.py shell
```

### **MySQL**

```bash
# Acceder a MySQL
mysql -u hospital -p -h localhost neonatal

# Dentro de MySQL:
SHOW TABLES;                    # Listar tablas
DESCRIBE roles_customuser;      # Ver estructura
SELECT * FROM roles_customuser; # Ver usuarios
```

### **Nginx**

```bash
# Validar configuración
sudo nginx -t

# Recargar sin detener
sudo systemctl reload nginx

# Reiniciar
sudo systemctl restart nginx

# Ver configuración activa
cat /etc/nginx/sites-available/neonatal
```

### **Backups**

```bash
# Hacer backup manual
MYSQL_PASSWORD='inacap' /home/hospital/backup-mysql.sh

# Ver backups realizados
ls -lh /home/hospital/neonatal-backups/

# Ver logs de backups
cat /var/log/neonatal-backup.log

# Restaurar un backup
gunzip < /home/hospital/neonatal-backups/neonatal_backup_*.sql.gz | \
  mysql -u hospital -p -h localhost neonatal
```

---

## 🎯 RESUMEN DEL FLUJO COMPLETO

```
USUARIO EN NAVEGADOR
        ↓
http://sistema.neonatal/ o http://10.155.12.62/
        ↓
NGINX (Servidor Web)
    ├─ ¿Archivo estático? → Sirve desde /staticfiles/
    └─ ¿URL dinámica? → Reenvía a Gunicorn
        ↓
GUNICORN (App Server)
    ├─ Despierta un worker
    └─ Ejecuta Django
        ↓
DJANGO
    ├─ Lee urls.py → Encuentra la vista
    ├─ Ejecuta view.py → Procesa lógica
    ├─ Consulta MySQL → Obtiene datos
    ├─ Renderiza template → Genera HTML
    └─ Devuelve respuesta
        ↓
GUNICORN
    └─ Envía respuesta a Nginx
        ↓
NGINX
    └─ Envía respuesta al navegador
        ↓
NAVEGADOR DEL USUARIO
    └─ Muestra página con estilos y scripts
```

---

## 📋 CHECKLIST DE ARRANQUE

Para que todo funcione correctamente, sigue este orden:

- [ ] 1. Verificar que MySQL está corriendo: `sudo systemctl status mysql`
- [ ] 2. Verificar que Gunicorn está corriendo: `sudo systemctl status gunicorn-neonatal`
- [ ] 3. Verificar que Nginx está corriendo: `sudo systemctl status nginx`
- [ ] 4. Verificar que Samba está corriendo: `sudo systemctl status smbd nmbd`
- [ ] 5. Acceder a `http://127.0.0.1/` en el navegador
- [ ] 6. Iniciar sesión con credenciales
- [ ] 7. Navegar al dashboard según el rol

---

## 🚨 SOLUCIÓN DE PROBLEMAS

| Problema | Causa | Solución |
|----------|-------|----------|
| "Conexión rechazada" | Nginx no está corriendo | `sudo systemctl restart nginx` |
| "TemplateDoesNotExist" | Templates con nombres incorrectos | Verificar mayúsculas/minúsculas |
| "Permission denied" en CSS | Permisos de lectura incorrectos | `sudo chmod o+rx /var/lib/mysql` |
| BD no conecta | MySQL no inició | `sudo systemctl restart mysql` |
| Backups no se crean | Cron no ejecutó | Verificar `sudo crontab -l` y logs |

---

**FIN DEL INFORME**

Este documento contiene toda la información necesaria para entender, gestionar y mantener el despliegue de Django Neonatal en LAN.

Fecha de elaboración: 17 de diciembre de 2025
