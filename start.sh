#!/usr/bin/env bash
set -e

echo "--> Fetching latest Tailscale version..."
# Fetch the latest stable version number directly from Tailscale's official endpoint
TAILSCALE_VERSION=$(curl -s https://pkgs.tailscale.com/stable/ | grep -oP 'tailscale_\K[0-9]+\.[0-9]+\.[0-9]+(?=_amd64\.tgz)' | head -n 1)

if [ -z "$TAILSCALE_VERSION" ]; then
  # Fallback version if dynamic extraction fails
  TAILSCALE_VERSION="1.76.6"
fi

echo "--> Downloading Tailscale static binary (v${TAILSCALE_VERSION})..."
TARBALL="tailscale_${TAILSCALE_VERSION}_amd64.tgz"
DOWNLOAD_URL="https://pkgs.tailscale.com/stable/${TARBALL}"

# Download the tarball directly
curl -fsSL "$DOWNLOAD_URL" -o "$TARBALL"

# Extract archive content
tar xzf "$TARBALL"

# Move the actual binaries out of the extracted directory into root
cp "tailscale_${TAILSCALE_VERSION}_amd64/tailscale" ./tailscale
cp "tailscale_${TAILSCALE_VERSION}_amd64/tailscaled" ./tailscaled

# Cleanup downloaded folder & tarball
rm -rf "tailscale_${TAILSCALE_VERSION}_amd64" "$TARBALL"

chmod +x ./tailscale ./tailscaled

echo "--> Starting tailscaled daemon..."
./tailscaled --tun=userspace-networking --socks5-server=localhost:10555 &

# Wait for tailscaled daemon to launch
sleep 3

echo "--> Connecting to Tailnet..."
./tailscale up --authkey="${TAILSCALE_AUTHKEY}" --hostname=render-app

echo "--> Starting main Python application..."
python app.py
