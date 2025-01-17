#!/bin/bash

cd /home/adesoji/Documents/cambsubmission/multi-tenant-kv-store || exit

echo "Removing all Docker images..."
docker rmi -f $(docker images -q) || echo "No images to remove."

sleep 45

echo "Pruning Docker volumes..."
docker volume prune -f

sleep 45


echo "Pruning Docker containers..."
docker container prune -f

sleep 45


echo "Performing a full system prune..."
docker system prune -a -f --volumes

sleep 45


echo "Building multitenant image..."
docker build --no-cache -t adesojialu/multitenant:latest . || exit
sleep 45
echo "Pushing multitenant image..."
docker push adesojialu/multitenant:latest || exit
sleep 15


echo "Building Huey image..."
docker build --no-cache -t adesojialu/hueyimage:latest -f Dockerfile.huey . || exit
sleep 45
echo "Pushing Huey image..."
docker push adesojialu/hueyimage:latest || exit

sleep 15


echo "Building Locust image..."
docker build --no-cache -t adesojialu/locust:latest -f Dockerfile.locust . || exit

sleep 45
echo "Pushing Locust image..."
docker push adesojialu/locust:latest || exit

sleep 15

echo "All images built and pushed successfully."
