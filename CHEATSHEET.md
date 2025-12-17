# 📋 CHEAT SHEET - Demostración Neonatal

## Comandos Rápidos para Copiar/Pegar

### 🚀 Opción 1: Demo Rápida (10 segundos)
```bash
cd /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5
./demo_quick.sh
```

### 🔍 Opción 2: Demo Completa (30 segundos)
```bash
cd /home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5
./test_demo.sh
```

### 📖 Ver Guía Rápida
```bash
cat QUICK_START_DEMO.md
```

### 🌐 Acceder al Sistema
```
URL: http://sistema.neonatal
Usuario: supervisor1
Contraseña: Inacap2025*
```

---

## Verificaciones Rápidas

### ¿Está MySQL activo?
```bash
systemctl status mysql
```

### ¿Está Nginx activo?
```bash
systemctl status nginx
```

### ¿Está Gunicorn activo?
```bash
systemctl status gunicorn-neonatal
```

### ¿Están los backups configurados?
```bash
ls -lh /home/hospital/neonatal-backups/
```

### Ver últimos logs de aplicación
```bash
journalctl -u gunicorn-neonatal -n 20
```

---

## Si Algo Falla

### Reiniciar Gunicorn
```bash
sudo systemctl restart gunicorn-neonatal
```

### Reiniciar Nginx
```bash
sudo systemctl restart nginx
```

### Verificar configuración Nginx
```bash
sudo nginx -t
```

---

## Usuarios para Demostración

Todos con contraseña: `Inacap2025*`

| Usuario | Rol |
|---------|-----|
| supervisor1 | SUPERVISOR |
| admin1 | ADMIN |
| matrona1 | MATRONA |
| auditor1 | AUDITORIA |
| exempleado | SOME |

---

## Info del Sistema

**IP del Servidor**: 10.155.12.62  
**BD**: MySQL (localhost:3306)  
**App**: Django + Gunicorn  
**Web**: Nginx  
**Compartición**: SAMBA

---

## Archivos Importantes

- `test_demo.sh` → Demo completa
- `demo_quick.sh` → Demo rápida
- `QUICK_START_DEMO.md` → Guía de inicio
- `DEMO_SCRIPTS_README.md` → Documentación completa
- `BACKUPS_SAMBA_GUIDE.md` → Información de backups

---

**¡Listo para demostrar! 🎯**
