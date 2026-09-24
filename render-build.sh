#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Download and extract Tailscale binaries
TAILSCALE_VERSION="1.56.1"
echo "--> Downloading Tailscale v${TAILSCALE_VERSION}..."

curl -sSL "https://pkgs.tailscale.com/stable/tailscale_${TAILSCALE_VERSION}_amd64.tar.gz" -o tailscale.tar.gz
tar xzf tailscale.tar.gz --strip-components=1 "tailscale_${TAILSCALE_VERSION}_amd64/tailscale" "tailscale_${TAILSCALE_VERSION}_amd64/tailscaled"
rm tailscale.tar.gz

# Make binaries executable
chmod +x tailscale tailscaled
echo "--> Tailscale binaries successfully installed!"
