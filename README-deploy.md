# Despliegue local LAN con Gunicorn + Nginx

Este repositorio incluye un pequeño helper para desplegar la app Django en la red local (LAN) usando `gunicorn` + `nginx` y un socket Unix. Está pensado para entornos de desarrollo/QA en una red local, no para producción pública.

Pasos automáticos (recomendado):

1. Desde la raíz del repositorio ejecuta (como `sudo`):

```bash
sudo ./deploy/deploy_local.sh
```

Esto copia el unit de `systemd` y la configuración de nginx a `/etc`, establece permisos sobre `staticfiles`, recarga `systemd`, habilita y arranca `gunicorn-neonatal` y reinicia `nginx`.

2. Comprobar servicios:

```bash
sudo systemctl status gunicorn-neonatal
sudo systemctl status nginx
```

3. Logs útiles:

```bash
sudo journalctl -u gunicorn-neonatal -n 200 --no-pager
sudo tail -n 200 /var/log/nginx/error.log
```

Notas importantes:
- El `systemd` unit está configurado para ejecutar Gunicorn como `User=hospital` y `Group=www-data`. Ajusta eso si tu usuario difiere.
- `STATIC_ROOT` ya está definido en `neonatal/settings.py`. Ejecuta `python manage.py collectstatic --noinput` desde el virtualenv si añades nuevos archivos estáticos.
- El `settings.py` ahora usa `DEBUG` desde `.env` con valor por defecto `False`. Para debug temporal añade `DEBUG=True` en tu `.env`.
- El script y las configuraciones requieren privilegios `sudo` para copiar a `/etc` y recargar servicios.

Si prefieres que lo haga yo (ejecutarlo aquí), necesito que pegues el password `sudo` en la terminal cuando te lo solicite — por seguridad prefiero que ejecutes el script localmente.
