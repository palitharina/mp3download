#!/usr/bin/env bash

# 1. Download Tailscale static binaries if missing
if [ ! -f ./tailscaled ]; then
    echo "--> Downloading Tailscale static binary..."
    TAILSCALE_VERSION="1.56.1"
    curl -sSL "https://pkgs.tailscale.com/stable/tailscale_${TAILSCALE_VERSION}_amd64.tar.gz" -o tailscale.tar.gz
    tar xzf tailscale.tar.gz --strip-components=1 "tailscale_${TAILSCALE_VERSION}_amd64/tailscale" "tailscale_${TAILSCALE_VERSION}_amd64/tailscaled"
    rm -f tailscale.tar.gz
    chmod +x tailscale tailscaled
fi

mkdir -p /tmp/tailscale
rm -f /tmp/tailscale/tailscaled.state

echo "--> Starting tailscaled daemon..."
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

sleep 5

echo "--> Connecting to Tailnet..."
./tailscale up --authkey="${TAILSCALE_AUTHKEY}" --hostname="render-app"

# Check if tailscale connected
if [ $? -ne 0 ]; then
    echo "--> ERROR: Tailscale authentication failed! Check your TAILSCALE_AUTHKEY environment variable."
    exit 1
fi

echo "--> Tailscale connected successfully!"

# Ensure SOCKS port is listening before launching Python
sleep 3

python3 app.py
