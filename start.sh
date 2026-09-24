#!/usr/bin/env bash

# 1. Download Tailscale static binaries if they are missing
if [ ! -f ./tailscaled ]; then
    echo "--> Downloading Tailscale static binary..."
    TAILSCALE_VERSION="1.56.1"
    curl -sSL "https://pkgs.tailscale.com/stable/tailscale_${TAILSCALE_VERSION}_amd64.tar.gz" -o tailscale.tar.gz
    tar xzf tailscale.tar.gz --strip-components=1 "tailscale_${TAILSCALE_VERSION}_amd64/tailscale" "tailscale_${TAILSCALE_VERSION}_amd64/tailscaled"
    rm -f tailscale.tar.gz
    chmod +x tailscale tailscaled
fi

# 2. Setup state directory
mkdir -p /tmp/tailscale

# 3. Start tailscaled daemon in userspace mode
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

sleep 4

# 4. Connect to your Tailnet
./tailscale up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app"

sleep 3

# 5. Start your Python application
python3 app.py
