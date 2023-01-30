#!/bin/bash
# Get App directory
APP_ROOT=$(dirname $(dirname $(readlink -fm $0)))

# Activate local python venv
cd "$APP_ROOT" || exit

# Generate requirements file
pip freeze requirements > requirements.txt

# Build docker images
docker build -f docker/Dockerfile . -t app --target app
docker build -f docker/Dockerfile . -t app-worker --target app-worker
docker build -f docker/Dockerfile . -t app-scheduler --target app-scheduler