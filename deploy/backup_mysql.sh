#!/bin/bash
# Script de backup automático para MySQL - Neonatal
# Uso: Ejecutar diariamente via cron

BACKUP_DIR="/backup/neonatal/mysql"
DB_NAME="neonatal"
DB_USER="hospital"
DB_PASSWORD="inacap"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${TIMESTAMP}.sql"
RETENTION_DAYS=30

# Crear directorio si no existe
mkdir -p "$BACKUP_DIR"

# Realizar backup
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando backup de MySQL..." >> "$BACKUP_DIR/backup.log"

mysqldump -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$BACKUP_FILE" 2>> "$BACKUP_DIR/backup.log"

if [ $? -eq 0 ]; then
    # Comprimir backup
    gzip "$BACKUP_FILE"
    BACKUP_FILE="${BACKUP_FILE}.gz"
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Backup completado: $BACKUP_FILE (Tamaño: $FILE_SIZE)" >> "$BACKUP_DIR/backup.log"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ Error en backup de MySQL" >> "$BACKUP_DIR/backup.log"
    exit 1
fi

# Limpiar backups antiguos (más de 30 días)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Limpiando backups anteriores a $RETENTION_DAYS días..." >> "$BACKUP_DIR/backup.log"
find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Generar lista de backups disponibles
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backups disponibles:" >> "$BACKUP_DIR/backup.log"
ls -lh "$BACKUP_DIR"/*.sql.gz 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}' >> "$BACKUP_DIR/backup.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup finalizado correctamente." >> "$BACKUP_DIR/backup.log"
echo "" >> "$BACKUP_DIR/backup.log"

exit 0
