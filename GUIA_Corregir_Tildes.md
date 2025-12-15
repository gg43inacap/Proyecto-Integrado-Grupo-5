# 🔧 Guía de Corrección de Problemas de Codificación UTF-8

## Problema Identificado
Los caracteres especiales (tildes, ñ) se están corrompiendo y mostrando como:
- María → MarÃ­a
- González → GonzÃ¡lez
- Chillán → ChillÃ¡n

## Soluciones Implementadas

### 1. ✅ Configuración Django (settings.py)
- Agregado `DEFAULT_CHARSET = 'utf-8'`
- Configurado `FILE_CHARSET = 'utf-8'`
- Mejorada configuración de base de datos SQLite
- Configuración de locale para español

### 2. ✅ Template Base (base.html)
- Agregado `<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">`
- Mejorada declaración de codificación

### 3. ✅ Script de Corrección (fix_encoding.py)
- Script para corregir datos existentes en la base de datos
- Mapeo automático de caracteres mal codificados

## 📋 Pasos para Aplicar las Correcciones

### Paso 1: Reiniciar el Servidor Django
```bash
# Detener el servidor si está corriendo (Ctrl+C)
# Luego reiniciar:
python manage.py runserver
```

### Paso 2: Ejecutar Script de Corrección de Datos
```bash
# En la terminal, ejecutar:
python fix_encoding.py
```

### Paso 3: Verificar la Corrección
1. Acceder al sistema
2. Revisar que los nombres se muestren correctamente
3. Crear un nuevo registro con tildes para probar

### Paso 4: Limpiar Cache del Navegador
- Presionar `Ctrl + F5` para recargar completamente
- O usar `Ctrl + Shift + R`

## 🔍 Verificaciones Adicionales

### Si el problema persiste:

1. **Verificar la consola del navegador:**
   - Abrir Herramientas de Desarrollador (F12)
   - Revisar si hay errores de codificación

2. **Verificar formularios específicos:**
   - Revisar que los formularios envíen datos en UTF-8
   - Comprobar headers HTTP

3. **Verificar base de datos:**
   ```bash
   python manage.py shell
   ```
   ```python
   from gestion_some.models import Madre
   # Ver datos actuales
   for madre in Madre.objects.all()[:5]:
       print(f"{madre.nombre} {madre.apellido_paterno}")
   ```

## 🚀 Prevención Futura

### Para nuevos datos:
1. **Siempre usar UTF-8** en formularios
2. **Verificar la codificación** del archivo al guardar en editor
3. **Usar caracteres especiales** de prueba al crear registros

### Ejemplo de test:
- Nombre: "María José"
- Apellido: "González Peña"
- Ciudad: "Chillán"

Si estos se guardan y muestran correctamente, la configuración UTF-8 está funcionando.

## ⚠️ Notas Importantes

- Los cambios en `settings.py` requieren reinicio del servidor
- Los datos existentes requieren corrección manual con el script
- SQLite maneja UTF-8 automáticamente después de la configuración
- Asegurar que el editor de código esté configurado en UTF-8

## 📞 Problemas Adicionales

Si persisten los problemas:
1. Verificar que el sistema operativo tenga soporte UTF-8
2. Revisar la configuración del terminal/consola
3. Comprobar la configuración regional del sistema