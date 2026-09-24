#!/usr/bin/env bash

# 1. Start tailscaled daemon
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

sleep 3

# 2. Connect and route ALL outbound traffic through your Android Exit Node
# Replace 100.96.38.127 with your phone's actual Tailscale IP
./tailscale up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app" \
  --exit-node=100.96.38.127 \
  --exit-node-allow-lan-access

# 3. Start python application
python3 app.py
