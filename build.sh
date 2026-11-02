#!/usr/bin/env bash
# Builds the deployable artifact: dist/webapp.tar.gz
# Used by GitHub Actions (and works on any Linux/macOS machine).
set -euo pipefail

cd "$(dirname "$0")"

rm -rf dist
mkdir -p dist/staging

# Put everything the server needs into one folder
cp -r common webapp dist/staging/
cp webapp/requirements.txt dist/staging/
find dist/staging -name "__pycache__" -type d -prune -exec rm -rf {} +

# Pack it into one file
tar -czf dist/webapp.tar.gz -C dist/staging .
rm -rf dist/staging

echo "Built dist/webapp.tar.gz"
