#!/usr/bin/env bash
set -e

# Define static Tailscale version
TAILSCALE_VERSION="1.96.4"
TS_FILE="tailscale_${TAILSCALE_VERSION}_amd64.tgz"

echo "==> Downloading Tailscale static binary..."
curl -fsSL "https://pkgs.tailscale.com/stable/${TS_FILE}" -o "${TS_FILE}"

echo "==> Extracting Tailscale..."
tar xzf "${TS_FILE}" --strip-components=1
rm -f "${TS_FILE}"

echo "==> Setting permissions..."
chmod +x tailscale tailscaled

echo "==> Preparing state directory..."
mkdir -p /tmp/tailscale

echo "==> Starting tailscaled daemon..."
./tailscaled \
  --tun=userspace-networking \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

sleep 3

echo "==> Connecting to Tailscale network..."
./tailscale --socket=/tmp/tailscale/tailscaled.sock up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app"

echo "==> Tailscale connected successfully!"

# Start your Python Application
exec python app.py
