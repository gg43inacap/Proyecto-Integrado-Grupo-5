@echo off
echo ========================================
echo    SISTEMA DE TESTS COMPLETO - NEONATAL
echo ========================================
cd /d %~dp0
call .venv\Scripts\activate

echo.
echo 🧪 EJECUTANDO TESTS UNITARIOS DE DJANGO...
echo ----------------------------------------
python manage.py test

echo.
echo 🔍 EJECUTANDO TESTS FUNCIONALES DEL SISTEMA...
echo ----------------------------------------
python test_sistema_completo.py

echo.
echo 🎯 RESUMEN FINAL
echo ========================================
echo ✅ Tests unitarios Django completados
echo ✅ Tests funcionales del sistema completados  
echo.
echo 🚀 VERIFICACION COMPLETA FINALIZADA
echo ========================================
pause
