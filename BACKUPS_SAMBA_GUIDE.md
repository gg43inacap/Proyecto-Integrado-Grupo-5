# 📦 Guía de Backups - Sistema Neonatal

## Descripción General

El sistema Neonatal implementa un sistema automático de backups de la base de datos MySQL que se ejecuta diariamente a las **2:00 AM**.

Los backups se almacenan en **carpetas compartidas por SAMBA** para permitir acceso remoto desde otros equipos como:
- 🖥️ **Router con almacenamiento** (NAS integrado)
- 💾 **NAS independiente** (QNAP, Synology, etc)
- 🖨️ **Otro PC/Servidor**
- 📱 **Equipos en la red local**

---

## 📍 Ubicaciones de Backups

| Ubicación | Ruta | Descripción |
|-----------|------|-------------|
| **Local (Servidor)** | `/home/hospital/neonatal-backups/` | Backups accesibles localmente en el servidor |
| **SAMBA Compartida** | `/backup/neonatal/` | Backups accesibles por red (NAS, otros PC) |

---

## 🔧 Configuración SAMBA Actual

### Compartición 1: `neonatal-backups`
```
Ruta: /home/hospital/neonatal-backups
Usuario válido: hospital (grupo mysql también)
Permisos: Lectura/Escritura
Acceso: Red Local
```

### Compartición 2: `neonatal_backups`
```
Ruta: /backup/neonatal
Usuario válido: hospital
Permisos: Lectura/Escritura
Acceso: Red Local
```

---

## 💻 Acceso desde Diferentes Equipos

### 1️⃣ **Desde Linux**

```bash
# Montar manualmente
mkdir -p /mnt/neonatal-backups
sudo mount -t cifs //10.155.12.62/neonatal-backups /mnt/neonatal-backups \
  -o username=hospital,password=inacap,vers=3.0

# Acceder a los backups
ls -lh /mnt/neonatal-backups/
```

### 2️⃣ **Desde Windows**

1. Abre **Explorador de archivos**
2. En la barra de direcciones, escribe: `\\10.155.12.62\neonatal-backups`
3. Ingresa credenciales:
   - Usuario: `hospital`
   - Contraseña: `inacap`
4. ¡Listo! Podrás ver los backups

### 3️⃣ **Desde Mac**

```bash
# En Finder: Comando + K (Go > Connect to Server)
smb://hospital:inacap@10.155.12.62/neonatal-backups
```

### 4️⃣ **Desde NAS (QNAP, Synology, etc)**

1. Configura el NAS para que monte carpetas compartidas SMB
2. Datos de conexión:
   - **Servidor**: `10.155.12.62` (ajusta según tu red)
   - **Usuario**: `hospital`
   - **Contraseña**: `inacap`
   - **Compartición**: `neonatal-backups` o `neonatal_backups`

---

## 📅 Información sobre los Backups

### Automatización
- ⏰ **Tiempo de ejecución**: Diariamente a las **02:00 AM**
- 📊 **Retención**: Últimos **30 días** (se eliminan automáticamente los más antiguos)
- 🔄 **Formato**: Comprimido con `gzip` (.sql.gz)
- 📦 **Ubicación**: Se almacenan en ambas carpetas automáticamente

### Formato del Nombre de Archivo
```
neonatal_backup_YYYYMMDD_HHMMSS.sql.gz
Ejemplo: neonatal_backup_20251217_020000.sql.gz
```

### Ejemplo de Tamaño
- BD típica: ~8 KB comprimida (varía según datos)

---

## 🛠️ Restaurar un Backup

### Desde el Servidor (Linux)

```bash
# Descomprimir el backup
gunzip -c /home/hospital/neonatal-backups/neonatal_backup_20251217_020000.sql.gz > backup.sql

# Restaurar en la BD
mysql -u hospital -p -h localhost neonatal < backup.sql
# Ingresa contraseña: inacap
```

### Desde otro PC

1. Descarga el archivo `.sql.gz` desde la compartición SAMBA
2. Descomprímelo
3. Usa tu cliente MySQL favorito para restaurar:
   ```bash
   mysql -u hospital -p -h 10.155.12.62 neonatal < backup.sql
   ```

---

## 📋 Log de Backups

El registro de ejecuciones se encuentra en:
```
/var/log/neonatal-backup.log
```

Para ver los últimos backups:
```bash
tail -50 /var/log/neonatal-backup.log
```

---

## ⚙️ Tareas Cron Configuradas

Ejecuta manualmente el backup:
```bash
/home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5/deploy/backup_mysql_neonatal.sh
```

Ver cron configurado:
```bash
crontab -l | grep backup
```

---

## 🔐 Credenciales y Seguridad

| Elemento | Valor |
|----------|-------|
| **Usuario MySQL** | `hospital` |
| **Contraseña MySQL** | `inacap` |
| **Usuario SAMBA** | `hospital` |
| **Contraseña SAMBA** | `inacap` |
| **Servidor** | `10.155.12.62` (ajusta según tu configuración) |
| **Puerto MySQL** | `3306` |

⚠️ **Nota**: Estos valores pueden ser modificados por el cliente final según sus políticas de seguridad.

---

## 🔄 Configuración para NAS/Router

### Opción 1: QNAP NAS
1. Configurar como destino SMB
2. Usuario: `hospital` | Contraseña: `inacap`
3. Los backups se copiarán automáticamente

### Opción 2: Router con Almacenamiento USB
1. Conectar USB al router
2. Configurar compartición SAMBA en el router
3. Configurar punto de montaje en el servidor Neonatal

### Opción 3: PC Secundario
1. Compartir carpeta en la red
2. Configurar montaje SMB en el servidor Neonatal
3. Los backups se sincronizan automáticamente

---

## 📞 Soporte y Mantenimiento

Para:
- ❌ Resolver problemas de conectividad SAMBA
- ✏️ Cambiar credenciales
- 🔧 Modificar horarios de backup
- 📦 Ajustar retención de backups

**Contacta al administrador del sistema**

---

## ✅ Verificación Final

Para verificar que todo está funcionando:

```bash
# 1. Verificar que MySQL está activo
systemctl status mysql

# 2. Verificar SAMBA
systemctl status smbd

# 3. Listar backups disponibles
ls -lh /home/hospital/neonatal-backups/
ls -lh /backup/neonatal/

# 4. Ver último log de backup
tail -20 /var/log/neonatal-backup.log
```

---

**Documento generado**: 17 de Diciembre de 2025  
**Sistema**: Neonatal - Hospital Herminda Martin  
**Versión**: 1.0
