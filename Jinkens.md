#!/bin/bash
set -e

CONTAINER_NAME="container_name"

# Stop and remove the container if it exists
if docker ps -a --format '{{.Names}}' | grep "$CONTAINER_NAME"; then
    docker stop "$CONTAINER_NAME"
    docker rm -f "$CONTAINER_NAME"
fi

# Remove the image if it exists
if docker images --format '{{.Repository}}' | grep "$CONTAINER_NAME"; then
    docker rmi -f "$CONTAINER_NAME"
fi

# Build the new image
if docker build -t "$CONTAINER_NAME" .; then
    echo "Image built successfully."
else
    echo "Failed to build the image."
    exit 1
fi

# Deploy the new container
if docker run -d --restart always --name "$CONTAINER_NAME" "$CONTAINER_NAME" python /code/app/main.py; then
    echo "Container deployed successfully."
else
    echo "Failed to deploy the container."
    exit 1
fi

# Clean up stopped containers and unused images
docker container prune -f
docker image prune -f
