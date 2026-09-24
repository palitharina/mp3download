#!/usr/bin/env bash

# Clear old state if any exists
rm -rf /tmp/tailscale/tailscaled.state

# 1. Start tailscaled daemon in userspace networking mode
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

# Wait for daemon to create socket
sleep 4

# 2. Connect to Tailnet with Exit Node
# Replace 100.96.38.127 with your phone's actual Tailscale IP
./tailscale up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app" \
  --exit-node=100.96.38.127 \
  --exit-node-allow-lan-access \
  --accept-routes=true

# Give Tailscale time to complete handshakes with your phone
sleep 5

# 3. Start Python App
python3 app.py
