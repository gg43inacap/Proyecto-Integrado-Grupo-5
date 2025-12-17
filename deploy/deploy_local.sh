#!/usr/bin/env bash
# Small deploy helper to install systemd unit and nginx site for local LAN deployment.
# Run this script with sudo from the repo root: `sudo ./deploy/deploy_local.sh`

set -euo pipefail

PROJECT_DIR="/home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5"
SYSTEMD_UNIT_SRC="$PROJECT_DIR/deploy/gunicorn-neonatal.service"
SYSTEMD_UNIT_DST="/etc/systemd/system/gunicorn-neonatal.service"
NGINX_CONF_SRC="$PROJECT_DIR/deploy/nginx-neonatal.conf"
NGINX_CONF_DST="/etc/nginx/sites-available/neonatal"
NGINX_ENABLED_DST="/etc/nginx/sites-enabled/neonatal"

echo "Installing systemd unit to $SYSTEMD_UNIT_DST"
cp "$SYSTEMD_UNIT_SRC" "$SYSTEMD_UNIT_DST"
chmod 644 "$SYSTEMD_UNIT_DST"

echo "Creating runtime dir /run/gunicorn"
mkdir -p /run/gunicorn
chown root:www-data /run/gunicorn
chmod 0755 /run/gunicorn

echo "Installing nginx config to $NGINX_CONF_DST"
cp "$NGINX_CONF_SRC" "$NGINX_CONF_DST"
ln -sf "$NGINX_CONF_DST" "$NGINX_ENABLED_DST"

echo "Ensuring staticfiles directory exists and permissions"
mkdir -p "$PROJECT_DIR/staticfiles"
chown -R www-data:www-data "$PROJECT_DIR/staticfiles"
chmod -R 755 "$PROJECT_DIR/staticfiles"

echo "Reloading systemd and starting services"
systemctl daemon-reload
systemctl enable --now gunicorn-neonatal

echo "Testing nginx configuration"
nginx -t
systemctl restart nginx

echo "Deployment complete. Check services with:"
echo "  sudo systemctl status gunicorn-neonatal"
echo "  sudo systemctl status nginx"

echo "If something failed, view logs:"
echo "  sudo journalctl -u gunicorn-neonatal -n 200 --no-pager"
echo "  sudo tail -n 200 /var/log/nginx/error.log"

exit 0
