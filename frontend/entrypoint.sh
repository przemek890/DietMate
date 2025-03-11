#!/bin/sh
set -eu

##################################################
#TODO: Move it to the Next.js server.js file, because we can manage how we want to start with HTTP or HTTPS
# has_ssl=true
# CERT_FILE="./SSL/fullchain.pem"
# KEY_FILE="./SSL/privkey.pem"

# if [ -n "$SSL_CERT_BASE64" ]; then
#     echo "Dekodowanie certyfikatu SSL..."
#     echo "$SSL_CERT_BASE64" | base64 -d > "$CERT_FILE"
# else
#     echo "Brak certyfikatu SSL (SSL_CERT_BASE64)."
#     has_ssl=false
# fi

# if [ -n "$SSL_KEY_BASE64" ]; then
#     echo "Dekodowanie klucza SSL..."
#     echo "$SSL_KEY_BASE64" | base64 -d > "$KEY_FILE"
# else
#     echo "Brak klucza SSL (SSL_KEY_BASE64)."
#     has_ssl=false
# fi
##################################################

RUNTIME_ENV_PATH="./public/runtime-env.js"

if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup; then
    RUNTIME_ENV_PATH="./build/runtime-env.js"
fi

printf "window.REACT_APP_DOMAIN='%s';\n" "$REACT_APP_DOMAIN" > "$RUNTIME_ENV_PATH"

echo "Gateway application domain: $REACT_APP_DOMAIN"

sleep 1

echo "Starting Next.js server..."
exec node server.js
