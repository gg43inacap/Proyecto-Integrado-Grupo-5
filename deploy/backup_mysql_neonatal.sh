#!/bin/bash

# ============================================
# Script de Backup Automático - Base de Datos Neonatal
# ============================================
# Este script realiza backups diarios de la BD MySQL del sistema Neonatal
# Los backups se almacenan en carpetas compartidas por SAMBA para fácil acceso
# desde otros equipos (NAS, Router con almacenamiento, PC, etc)
#
# Uso: ./backup_mysql_neonatal.sh
# Automatización: Agregar a crontab para ejecutar diariamente
# Ejemplo cron: 0 2 * * * /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5/deploy/backup_mysql_neonatal.sh >> /var/log/neonatal-backup.log 2>&1
# ============================================

set -e

# ============ CONFIGURACIÓN ============
DB_NAME="neonatal"
DB_USER="hospital"
DB_PASSWORD="inacap"
DB_HOST="localhost"
DB_PORT="3306"

# Directorios de backup
BACKUP_DIR_LOCAL="/home/hospital/neonatal-backups"
BACKUP_DIR_SAMBA="/backup/neonatal"

# Nombre del archivo de backup con timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE_NAME="neonatal_backup_${TIMESTAMP}.sql.gz"

# Retención de backups (en días)
RETENTION_DAYS=30

# Log del script
LOG_FILE="/var/log/neonatal-backup.log"

# ============ FUNCIONES ============

log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] ${message}" | tee -a "$LOG_FILE" 2>/dev/null || echo "[${timestamp}] ${message}"
}

create_backup() {
    log_message "=========================================="
    log_message "Iniciando backup de base de datos Neonatal"
    log_message "=========================================="
    
    # Crear carpetas si no existen
    mkdir -p "$BACKUP_DIR_LOCAL"
    mkdir -p "$BACKUP_DIR_SAMBA"
    
    # Realizar backup
    log_message "Exportando base de datos: $DB_NAME"
    BACKUP_PATH_LOCAL="${BACKUP_DIR_LOCAL}/${BACKUP_FILE_NAME}"
    
    if mysqldump \
        --user="$DB_USER" \
        --password="$DB_PASSWORD" \
        --host="$DB_HOST" \
        --port="$DB_PORT" \
        --single-transaction \
        --quick \
        --lock-tables=false \
        "$DB_NAME" | gzip > "$BACKUP_PATH_LOCAL"; then
        
        log_message "✓ Backup exitoso: $BACKUP_FILE_NAME"
        log_message "  Tamaño: $(du -h "$BACKUP_PATH_LOCAL" | cut -f1)"
        
        # Copiar a carpeta SAMBA
        cp "$BACKUP_PATH_LOCAL" "$BACKUP_DIR_SAMBA/$BACKUP_FILE_NAME"
        log_message "✓ Backup copiado a carpeta compartida SAMBA"
        
        return 0
    else
        log_message "✗ Error durante el backup"
        return 1
    fi
}

cleanup_old_backups() {
    log_message "Limpiando backups antiguos (reteniendo últimos $RETENTION_DAYS días)"
    
    # Limpiar en directorio local
    find "$BACKUP_DIR_LOCAL" -name "neonatal_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    local deleted_local=$(find "$BACKUP_DIR_LOCAL" -name "neonatal_backup_*.sql.gz" -mtime +$RETENTION_DAYS | wc -l)
    
    if [ $deleted_local -gt 0 ]; then
        log_message "✓ Eliminados $deleted_local backups antiguos del directorio local"
    fi
    
    # Limpiar en directorio SAMBA
    find "$BACKUP_DIR_SAMBA" -name "neonatal_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    local deleted_samba=$(find "$BACKUP_DIR_SAMBA" -name "neonatal_backup_*.sql.gz" -mtime +$RETENTION_DAYS | wc -l)
    
    if [ $deleted_samba -gt 0 ]; then
        log_message "✓ Eliminados $deleted_samba backups antiguos del directorio SAMBA"
    fi
}

verify_connectivity() {
    log_message "Verificando conectividad con MySQL..."
    
    if mysql --user="$DB_USER" --password="$DB_PASSWORD" --host="$DB_HOST" --port="$DB_PORT" -e "SELECT 1" > /dev/null 2>&1; then
        log_message "✓ Conexión a MySQL exitosa"
        return 0
    else
        log_message "✗ No se puede conectar a MySQL"
        return 1
    fi
}

generate_report() {
    log_message "=========================================="
    log_message "REPORTE DE BACKUP"
    log_message "=========================================="
    
    log_message "Backups disponibles en $BACKUP_DIR_LOCAL:"
    ls -lh "$BACKUP_DIR_LOCAL"/neonatal_backup_*.sql.gz 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}' || log_message "  No hay backups"
    
    log_message "Backups disponibles en $BACKUP_DIR_SAMBA (SAMBA):"
    ls -lh "$BACKUP_DIR_SAMBA"/neonatal_backup_*.sql.gz 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}' || log_message "  No hay backups"
    
    log_message "=========================================="
}

# ============ EJECUCIÓN PRINCIPAL ============

# Verificar si se ejecuta como root o con permisos suficientes
if [ "$EUID" -ne 0 ] && [ "$USER" != "hospital" ]; then 
    log_message "✗ Este script debe ejecutarse como 'hospital' o con sudo"
    exit 1
fi

# Ejecutar funciones
if verify_connectivity; then
    if create_backup; then
        cleanup_old_backups
        generate_report
        log_message "✓ Backup completado exitosamente"
        exit 0
    else
        log_message "✗ Error: No se pudo crear el backup"
        exit 1
    fi
else
    log_message "✗ Error: No hay conectividad con MySQL"
    exit 1
fi
