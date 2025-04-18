#!/bin/bash
set -a
source ./server/.env
set +a

# Function to free a port if occupied by a Docker container
free_port() {
  port=$1
  container_id=$(docker ps -q --filter "publish=$port")

  if [ -n "$container_id" ]; then
    echo "Releasing port $port (used by container $container_id)..."
    docker stop "$container_id"
    docker rm "$container_id"
  fi
}

# Free ports
free_port 5432
free_port 8000
free_port 3000

echo "Stopping existing containers..."
docker-compose down # Ensure all services defined in the compose file are stopped and removed

echo "Building and starting containers..."
docker-compose up --build # Add --build flag to force rebuilding images
