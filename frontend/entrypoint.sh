#!/bin/sh

has_ssl=true
CERT_FILE="./SSL/fullchain.pem"
KEY_FILE="./SSL/privkey.pem"

if [ -n "$SSL_CERT_BASE64" ]; then
    echo "Decoding SSL certificate..."
    echo "$SSL_CERT_BASE64" | base64 -d > "$CERT_FILE"
else
    echo "Missing SSL certificate (SSL_CERT_BASE64)."
    has_ssl=false
fi

if [ -n "$SSL_KEY_BASE64" ]; then
    echo "Decoding SSL key..."
    echo "$SSL_KEY_BASE64" | base64 -d > "$KEY_FILE"
else
    echo "Missing SSL key (SSL_KEY_BASE64)."
    has_ssl=false
fi

echo "Gateway application domain: $NEXT_PUBLIC_DOMAIN"

sleep 1

echo "Starting Remix server..."
exec npm start
