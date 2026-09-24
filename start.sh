#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "==> Downloading and installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sh

echo "==> Starting tailscaled daemon..."
tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &

# Wait briefly for daemon to initialize
sleep 3

echo "==> Connecting Render to Tailscale network..."
tailscale up --authkey=${TAILSCALE_AUTHKEY} --hostname=render-app

echo "==> Successfully connected to Tailscale network!"

# Launch your main Python app (change app.py to your main script file if needed)
exec python app.py


