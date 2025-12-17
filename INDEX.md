📚 ÍNDICE DE ARCHIVOS - DEMOSTRACIÓN SISTEMA NEONATAL
═════════════════════════════════════════════════════════════════════════════

🎯 PUNTO DE INICIO: Lee primero
───────────────────────────────────────────────────────────────────────────
📄 QUICK_START_DEMO.md
   └─ Guía rápida para demostración
   └─ Preguntas frecuentes
   └─ Credenciales
   Tiempo: 2 minutos de lectura

🚀 SCRIPTS EJECUTABLES
───────────────────────────────────────────────────────────────────────────
📜 ./demo_quick.sh (RECOMENDADO)
   └─ Demo rápida y visual
   └─ Ideal para presentaciones ejecutivas
   └─ Duración: ~10 segundos
   └─ Uso: ./demo_quick.sh

📜 ./test_demo.sh
   └─ Demo técnica completa
   └─ Ideal para verificación técnica
   └─ Duración: ~30 segundos
   └─ Uso: ./test_demo.sh

📖 DOCUMENTACIÓN DETALLADA
───────────────────────────────────────────────────────────────────────────
📖 DEMO_SCRIPTS_README.md
   └─ Documentación completa de los scripts
   └─ Escenarios de uso
   └─ Interpretación de resultados
   └─ Solución de problemas
   Tiempo: 5-10 minutos

📖 CHEATSHEET.md
   └─ Comandos listos para copiar/pegar
   └─ Verificaciones rápidas
   └─ Troubleshooting express
   Tiempo: 1 minuto

📖 BACKUPS_SAMBA_GUIDE.md
   └─ Sistema de backups automáticos
   └─ Acceso desde otros equipos
   └─ Procedimientos de restauración
   Tiempo: 5 minutos

═════════════════════════════════════════════════════════════════════════════

⏱️  FLUJO DE DEMOSTRACIÓN RECOMENDADO:

1️⃣  ANTES DE LA DEMO (30 minutos antes)
   ├─ Lee: QUICK_START_DEMO.md (2 min)
   ├─ Ejecuta: ./demo_quick.sh (10 seg)
   └─ Si todo está bien, procede. Si no, consulta CHEATSHEET.md

2️⃣  INICIO DE LA DEMO (5 minutos)
   ├─ Ejecuta: ./demo_quick.sh
   ├─ Muestra: Output exitoso al cliente
   └─ Explica: "Sistema verificó que todo está operativo"

3️⃣  DURANTE LA DEMO (10-15 minutos)
   ├─ Abre: http://sistema.neonatal
   ├─ Login: supervisor1 / Inacap2025*
   ├─ Muestra: Dashboard, reportes, exportaciones
   └─ Explica: Sistema de backups automáticos

4️⃣  SI EL CLIENTE TIENE PREGUNTAS
   ├─ Técnicas: Consulta DEMO_SCRIPTS_README.md
   ├─ De backups: Consulta BACKUPS_SAMBA_GUIDE.md
   └─ Rápidas: Consulta CHEATSHEET.md

═════════════════════════════════════════════════════════════════════════════

🎯 SEGÚN EL TIPO DE CLIENTE:

CLIENTE EJECUTIVO/GERENCIAL
├─ Lee: QUICK_START_DEMO.md (punto "QUÉ MOSTRAR AL CLIENTE")
├─ Ejecuta: ./demo_quick.sh
├─ Muestra: Dashboard y reportes
└─ Duración: 5-10 minutos

CLIENTE TÉCNICO/TI
├─ Lee: DEMO_SCRIPTS_README.md (sección completa)
├─ Ejecuta: ./test_demo.sh
├─ Muestra: Todos los detalles técnicos
└─ Duración: 15-20 minutos

CLIENTE MÚLTIPLE (Ejecutivos + TI)
├─ Fase 1: Ejecuta ./demo_quick.sh para todos
├─ Fase 2: Muestra dashboard ejecutivo (5 min)
├─ Fase 3: Detalles técnicos para el equipo TI (consulta DEMO_SCRIPTS_README.md)
└─ Duración: 20-30 minutos

═════════════════════════════════════════════════════════════════════════════

✅ CHECKLIST PRE-DEMOSTRACIÓN:

Antes de ir a demostración, verifica:

□ Ejecuté ./demo_quick.sh y vio ✅ TODOS LOS TESTS
□ Abrí http://sistema.neonatal en navegador
□ Logré ingresar con supervisor1 / Inacap2025*
□ Vi el dashboard con datos
□ Pude descargar un reporte (Excel o PDF)
□ Tengo a mano QUICK_START_DEMO.md (referencia)
□ Tengo a mano CHEATSHEET.md (emergencias)
□ IP del servidor anotada (10.155.12.62)
□ Otro PC/Mac/Windows listo para SAMBA (opcional)

═════════════════════════════════════════════════════════════════════════════

🚨 EMERGENCIA: Algo no funciona

Si algo falla durante la demo:

1. PRIMER PASO: Abre CHEATSHEET.md
2. BUSCA: El problema específico
3. EJECUTA: El comando de solución
4. SI NO FUNCIONA: 
   └─ Explica: "El sistema detectó un problema y lo está resolviendo"
   └─ Ejecuta: sudo systemctl restart gunicorn-neonatal
   └─ Espera: 5 segundos
   └─ REINTENTAR: Acceder nuevamente a la URL

═════════════════════════════════════════════════════════════════════════════

📞 CONTACTO RÁPIDO:

Si necesitas ayuda durante la demo:

Problema: API no responde
   → Solución: sudo systemctl restart gunicorn-neonatal

Problema: No puedo acceder a la URL
   → Solución: Intenta con http://localhost

Problema: Se congela la página
   → Solución: sudo systemctl restart nginx

Problema: Error de base de datos
   → Solución: systemctl status mysql

═════════════════════════════════════════════════════════════════════════════

✨ ¡LISTO PARA DEMOSTRAR! ✨

Para iniciar:

1. Abre terminal
2. cd /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5
3. ./demo_quick.sh
4. ¡Que vaya bien! 🚀

═════════════════════════════════════════════════════════════════════════════

Documento creado: 17 de Diciembre de 2025
Estado: ✅ LISTO PARA DEMOSTRACIÓN
