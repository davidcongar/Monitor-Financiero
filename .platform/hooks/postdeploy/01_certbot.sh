#!/bin/bash

set -e

# Install Certbot and NGINX plugin
sudo dnf install -y certbot python3-certbot-nginx awscli

DOMAIN="monitorfinanciero.snappsolutions.com"
S3_BUCKET="snappsolutions"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"

# Try to download existing certs from S3
echo "Trying to download existing certs from S3..."
aws s3 sync "s3://$S3_BUCKET/letsencrypt/" /etc/letsencrypt/ || true

# Check if cert already exists
if [ -f "$CERT_PATH" ]; then
  echo "Certificate for $DOMAIN already exists. Skipping certbot."
else
  echo "Certificate not found. Running certbot..."
  sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m contacto@snappsolutions.com

  echo "Uploading newly created certs to S3..."
  aws s3 sync /etc/letsencrypt/ "s3://$S3_BUCKET/letsencrypt/"
  
  sudo systemctl restart nginx
fi
