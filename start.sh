#!/usr/bin/env bash

# Clean up any stale sockets or states
rm -rf /tmp/tailscale/tailscaled.state

# 1. Start tailscaled daemon with SOCKS5 binding
./tailscaled \
  --tun=userspace-networking \
  --socks5-server=127.0.0.1:10555 \
  --state=/tmp/tailscale/tailscaled.state \
  --socket=/tmp/tailscale/tailscaled.sock &

sleep 3

# 2. Connect to Tailnet standardly (No exit node flag)
./tailscale up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname="render-app"

sleep 3

# 3. Start Python App
python3 app.py
