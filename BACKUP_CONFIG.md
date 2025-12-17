# Configuración de Backup para NAS - Neonatal

## 📍 Ubicaciones de Datos

### Base de Datos MySQL
- **Directorio**: `/var/lib/mysql/`
- **Base de datos**: `neonatal`
- **Tamaño actual**: 0.56 MB
- **Tablas**: 15 tablas (auditoria, madres, partos, RN, reportes, usuarios, etc.)

### Carpeta de Backups
- **Directorio**: `/home/hospital/neonatal-backups/`
- **Descripción**: Backups diarios comprimidos en .sql.gz
- **Retención**: 30 días

---

## 🌐 Acceso Samba/SMB desde NAS

### Compartidos disponibles:

1. **mysql-data** (datos en vivo)
   - Ruta: `\\10.155.12.62\mysql-data`
   - Usuario: `hospital`
   - Contraseña: `inacap`
   - Descripción: Acceso directo a `/var/lib/mysql`

2. **neonatal-backups** (backups)
   - Ruta: `\\10.155.12.62\neonatal-backups`
   - Usuario: `hospital`
   - Contraseña: `inacap`
   - Descripción: Backups automáticos del sistema

---

## 🔐 Credenciales de Acceso

| Parámetro | Valor |
|-----------|-------|
| IP del servidor | `10.155.12.62` |
| Usuario Samba | `hospital` |
| Contraseña Samba | `inacap` |
| Usuario MySQL | `hospital` |
| Contraseña MySQL | `inacap` |
| Dominio local | `sistema.neonatal` |

---

## ⏰ Backup Automático

### Script: `/home/hospital/backup-mysql.sh`

**Funcionalidad:**
- Ejecuta diariamente a las 2:00 AM
- Exporta BD `neonatal` en formato SQL
- Comprime en .gz (reduce ~70% el tamaño)
- Elimina backups > 30 días
- Guarda logs en `/var/log/neonatal-backup.log`

**Cron actual:**
```
0 2 * * * MYSQL_PASSWORD='inacap' /home/hospital/backup-mysql.sh >> /var/log/neonatal-backup.log 2>&1
```

**Para modificar frecuencia:**
```bash
sudo crontab -e
```

Ejemplos:
- Diariamente 2:00 AM: `0 2 * * *`
- Cada 6 horas: `0 */6 * * *`
- Cada hora: `0 * * * *`

---

## 📊 Tablas de la Base de Datos

| Tabla | Descripción |
|-------|-------------|
| `roles_customuser` | Usuarios del sistema |
| `gestion_some_madre` | Datos de madres |
| `partos_parto` | Registros de partos |
| `partos_rn` | Recién nacidos |
| `reportes_reporte` | Reportes generados |
| `auditoria_auditoria` | Log de auditoría |
| `auth_*` | Tablas de autenticación Django |

---

## 🔧 Conexión desde NAS

### Linux/Mac
```bash
# Montar compartido
sudo mount -t cifs //10.155.12.62/neonatal-backups /mnt/neonatal-backups \
  -o username=hospital,password=inacap,uid=$(id -u),gid=$(id -g)

# Desmontar
sudo umount /mnt/neonatal-backups
```

### Windows
```
\\10.155.12.62\neonatal-backups
Credenciales: hospital / inacap
```

### QNAP/Synology NAS
1. Panel de Control → Carpeta compartida
2. Crear backup remoto SMB
3. Servidor: `10.155.12.62`
4. Carpeta: `neonatal-backups`
5. Usuario: `hospital`
6. Contraseña: `inacap`

---

## 📝 Notas Importantes

- **Seguridad**: Esta configuración es segura solo en LAN local
- **Permisos**: El usuario Samba solo puede acceder a esas 2 carpetas
- **Datos MySQL en vivo**: Accesible vía `mysql-data` pero mejor usar backups
- **Restauración**: Para restaurar, usar: 
  ```bash
  gunzip < backup.sql.gz | mysql -u hospital -p neonatal
  ```

---

**Última actualización**: 17 de diciembre de 2025
**Servidor**: neonatal (10.155.12.62)
**Versión MySQL**: 8.0.44
**Versión Django**: 5.2.8
