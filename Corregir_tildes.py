#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir problemas de codificación UTF-8 en la base de datos.
Ejecutar este script después de configurar UTF-8 en Django.
"""

import os
import django
import sys

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from gestion_some.models import Madre
from partos.models import Parto, RN

def fix_encoding_issues():
    """
    Corrige problemas de codificación en los datos existentes.
    """
    print("🔧 Iniciando corrección de codificación UTF-8...")
    
    # Mapeo de caracteres mal codificados a correctos usando códigos seguros
    replacements = {
        # Vocales minúsculas con tildes
        '\u00c3\u00a1': 'á',  # Ã¡ -> á
        '\u00c3\u00a9': 'é',  # Ã© -> é
        '\u00c3\u00ad': 'í',  # Ã­ -> í
        '\u00c3\u00b3': 'ó',  # Ã³ -> ó
        '\u00c3\u00ba': 'ú',  # Ãº -> ú
        # Eñe minúscula
        '\u00c3\u00b1': 'ñ',  # Ã± -> ñ
        # Vocales mayúsculas con tildes
        '\u00c3\u0081': 'Á',  # Ã -> Á
        '\u00c3\u0089': 'É',  # Ã‰ -> É
        '\u00c3\u008d': 'Í',  # Ã -> Í
        '\u00c3\u0093': 'Ó',  # Ã" -> Ó
        '\u00c3\u009a': 'Ú',  # Ãš -> Ú
        # Eñe mayúscula
        '\u00c3\u0091': 'Ñ',  # Ã' -> Ñ
        # Patrones comunes adicionales
        'MarÃ­a': 'María',
        'GonzÃ¡lez': 'González', 
        'ChillÃ¡n': 'Chillán',
    }
    
    def fix_string(text):
        """Corrige una cadena de texto."""
        if not text:
            return text
        
        fixed_text = str(text)
        for bad_char, good_char in replacements.items():
            fixed_text = fixed_text.replace(bad_char, good_char)
        return fixed_text
    
    # Corregir datos en modelo Madre
    print("📝 Corrigiendo datos de Madres...")
    madres_count = 0
    for madre in Madre.objects.all():
        updated = False
        
        # Corregir campos de texto (solo los que existen en el modelo)
        fields_to_fix = ['nombre', 'direccion', 'comuna', 'cesfam', 'antecedentes_obstetricos', 'alergias_si']
        for field in fields_to_fix:
            if hasattr(madre, field):
                original_value = getattr(madre, field)
                if original_value:
                    fixed_value = fix_string(original_value)
                    if fixed_value != original_value:
                        setattr(madre, field, fixed_value)
                        updated = True
                        print(f"  ✅ Corregido: {original_value} → {fixed_value}")
        
        if updated:
            madre.save()
            madres_count += 1
    
    # Corregir datos en modelo Parto (si hay campos de texto)
    print("📝 Corrigiendo datos de Partos...")
    partos_count = 0
    for parto in Parto.objects.all():
        updated = False
        
        # Si hay campos de texto en Parto, agregarlos aquí
        # Por ejemplo, si hay campos como 'observaciones', 'comentarios', etc.
        
        if updated:
            parto.save()
            partos_count += 1
    
    # Corregir datos en modelo RN
    print("📝 Corrigiendo datos de Recién Nacidos...")
    rn_count = 0
    for rn in RN.objects.all():
        updated = False
        
        # Corregir campos de texto en RN si los hay
        fields_to_fix = ['nombre']  # Agregar más campos según sea necesario
        for field in fields_to_fix:
            if hasattr(rn, field):
                original_value = getattr(rn, field)
                if original_value:
                    fixed_value = fix_string(original_value)
                    if fixed_value != original_value:
                        setattr(rn, field, fixed_value)
                        updated = True
                        print(f"  ✅ Corregido: {original_value} → {fixed_value}")
        
        if updated:
            rn.save()
            rn_count += 1
    
    print(f"\n🎉 Corrección completada:")
    print(f"  - Madres corregidas: {madres_count}")
    print(f"  - Partos corregidos: {partos_count}")
    print(f"  - RNs corregidos: {rn_count}")
    print("\n💡 Recomendaciones:")
    print("  1. Reinicia el servidor Django")
    print("  2. Limpia la caché del navegador")
    print("  3. Verifica que todos los formularios usen UTF-8")

if __name__ == "__main__":
    fix_encoding_issues()