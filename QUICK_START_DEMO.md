#!/bin/bash

# ============================================
# INICIO RÁPIDO - DEMO AL CLIENTE
# ============================================
# Este archivo es solo para referencia
# Guía rápida de qué ejecutar

cat << 'EOF'

🎬 GUÍA RÁPIDA PARA DEMOSTRACIÓN

═══════════════════════════════════════════════════════════════════

PASO 1: Abre una terminal en la raíz del proyecto

PASO 2: Ejecuta la demo rápida (recomendado)
   $ ./demo_quick.sh

   O si quieres ver más detalles:
   $ ./test_demo.sh

PASO 3: Espera 10-30 segundos

PASO 4: Verás ✅ SISTEMA LISTO PARA DEMOSTRACIÓN

═══════════════════════════════════════════════════════════════════

PASO 5: Abre el navegador y accede a:
   http://sistema.neonatal

   Si no funciona, usa:
   http://localhost
   O la IP del servidor: http://10.155.12.62

PASO 6: Inicia sesión con:
   Usuario: supervisor1
   Contraseña: Inacap2025*

═══════════════════════════════════════════════════════════════════

QUÉ MOSTRAR AL CLIENTE:

1. Dashboard Supervisor
   → Muestra estadísticas en tiempo real
   → Gráficos interactivos

2. Reportes REM A24
   → Datos filtrados por mes/año
   → Botones de exportación a Excel/PDF

3. Acceso desde otros equipos
   → Mostrar compartición SAMBA
   → Acceso a backups desde otro PC (Windows/Mac)

4. Usuarios diferentes
   → Login con otros usuarios
   → Mostrar roles diferentes

═══════════════════════════════════════════════════════════════════

CREDENCIALES ADICIONALES PARA DEMOSTRAR:

   admin1 / Inacap2025*        (ADMIN)
   matrona1 / Inacap2025*      (MATRONA)
   auditor1 / Inacap2025*      (AUDITORIA)
   exempleado / Inacap2025*    (SOME)

═══════════════════════════════════════════════════════════════════

SI ALGO FALLA:

1. Verifica que todos los servicios están activos:
   $ systemctl status mysql
   $ systemctl status nginx
   $ systemctl status gunicorn-neonatal

2. Si no funciona, reinicia:
   $ sudo systemctl restart gunicorn-neonatal
   $ sudo systemctl restart nginx

3. Para verificar logs:
   $ journalctl -u gunicorn-neonatal -n 20

═══════════════════════════════════════════════════════════════════

DURACIÓN RECOMENDADA DE DEMOSTRACIÓN:

Quick Demo:        5-10 minutos
Full Demo:         15-20 minutos
Con preguntas:     20-30 minutos

═══════════════════════════════════════════════════════════════════

¿PREGUNTAS COMUNES DEL CLIENTE?

P: ¿Dónde están mis datos?
R: En MySQL, en la carpeta /var/lib/mysql/
   Los backups están en /home/hospital/neonatal-backups/

P: ¿Cómo accedo desde otro PC?
R: Usa la URL http://[IP_DEL_SERVIDOR]
   O monta la compartición SAMBA para los backups

P: ¿Cómo hago backups?
R: Automático cada día a las 2 AM
   Mira el archivo BACKUPS_SAMBA_GUIDE.md

P: ¿Qué usuarios hay?
R: Los que quieras crear. Actualmente:
   - admin1 (Administrador)
   - supervisor1 (Supervisor de reportes)
   - matrona1 (Matrona)
   - auditor1 (Auditor)
   - exempleado (Operador SOME)

═══════════════════════════════════════════════════════════════════

DOCUMENTACIÓN DISPONIBLE:

- DEMO_SCRIPTS_README.md       (Este archivo)
- BACKUPS_SAMBA_GUIDE.md       (Sistema de backups)
- README.md                    (General del proyecto)
- INFORME_DESPLIEGUE_COMPLETO.md (Detalles técnicos)

═══════════════════════════════════════════════════════════════════

BUENA SUERTE EN LA DEMO! 🎯

EOF
