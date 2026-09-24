#!/usr/bin/env bash
set -e

# 1. Create a writable directory in /tmp for runtime files
mkdir -p /tmp/tailscale

echo "--> Fetching latest Tailscale version..."
TAILSCALE_VERSION=$(curl -s https://pkgs.tailscale.com/stable/ | grep -oP 'tailscale_\K[0-9]+\.[0-9]+\.[0-9]+(?=_amd64\.tgz)' | head -n 1)

if [ -z "$TAILSCALE_VERSION" ]; then
  TAILSCALE_VERSION="1.76.6"
fi

echo "--> Downloading Tailscale static binary (v${TAILSCALE_VERSION})..."
TARBALL="tailscale_${TAILSCALE_VERSION}_amd64.tgz"
curl -fsSL "https://pkgs.tailscale.com/stable/${TARBALL}" -o "$TARBALL"

tar xzf "$TARBALL"
cp "tailscale_${TAILSCALE_VERSION}_amd64/tailscale" ./tailscale
cp "tailscale_${TAILSCALE_VERSION}_amd64/tailscaled" ./tailscaled
rm -rf "tailscale_${TAILSCALE_VERSION}_amd64" "$TARBALL"

chmod +x ./tailscale ./tailscaled

echo "--> Starting tailscaled daemon..."
# Direct socket and state files to writable /tmp directory
./tailscaled \
  --tun=userspace-networking \
  --socket=/tmp/tailscale/tailscaled.sock \
  --state=/tmp/tailscale/tailscaled.state \
  --socks5-server=localhost:10555 &

# Give the daemon a moment to initialize the socket
sleep 3

echo "--> Connecting to Tailnet..."
# Pass --socket flag so the CLI can talk to tailscaled at the custom path
./tailscale --socket=/tmp/tailscale/tailscaled.sock up \
  --authkey="${TAILSCALE_AUTHKEY}" \
  --hostname=render-app

echo "--> Starting main Python application..."
python app.py
