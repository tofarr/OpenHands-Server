#!/bin/bash

# Build script for OpenHands Server
# Based on OpenHands-CLI build script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse command line arguments
INSTALL_PYINSTALLER=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --install-pyinstaller)
            INSTALL_PYINSTALLER=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--install-pyinstaller]"
            exit 1
            ;;
    esac
done

echo "Building OpenHands Server..."

# Install PyInstaller if requested
if [ "$INSTALL_PYINSTALLER" = true ]; then
    echo "Installing PyInstaller..."
    uv add --dev pyinstaller
fi

# Ensure we have development dependencies
echo "Installing dependencies..."
uv sync --extra dev

# Run the build
echo "Running PyInstaller..."
uv run python build.py

echo "Build complete!"
echo "Binary location: dist/openhands-server"