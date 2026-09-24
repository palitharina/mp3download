#!/usr/bin/env bash
set -e

TAILSCALE_VERSION="1.96.4"
TS_FILE="tailscale_${TAILSCALE_VERSION}_amd64.tgz"

if [ -z "${TAILSCALE_AUTHKEY}" ]; then
  echo "ERROR: TAILSCALE_AUTHKEY environment variable is not set in Render!"
  exit 1
fi

if [ ! -f ./tailscaled ]; then
  echo "==> Downloading Tailscale static binary..."
  curl -fsSL "https://pkgs.tailscale.com/stable/${TS_FILE}" -o "${TS_FILE}"
  tar xzf "${TS_FILE}" --strip-components=1
  rm -f "${TS_FILE}"
  chmod +x tailscale tailscaled
fi

mkdir -p /tmp/tailscale

echo "==> Starting tailscaled daemon..."
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

# Wait for daemon socket
sleep 3

echo "==> Connecting to Tailscale network..."
./tailscale --socket=/tmp/tailscale/tailscaled.sock up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app" \
  --accept-routes

echo "==> Tailscale connected successfully!"

# Execute Python app
exec python app.py
