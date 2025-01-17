#!/bin/bash
cd ~/Documents/cambsubmission/multi-tenant-kv-store/k8s || exit

echo "Deleting FastAPI, Huey, Grafana, and Prometheus deployments..."
sleep 30
kubectl delete deployment fastapi
sleep 30
kubectl delete deployment huey
sleep 30
kubectl delete deployment grafana
sleep 30
kubectl delete deployment prometheus
sleep 30

echo "Deleting Redis StatefulSet and Service..."
kubectl delete statefulset redis

kubectl delete service redis


echo "Verifying that all pods have been removed..."
kubectl get pods


echo "Deleting Persistent Volume Claims (PVCs)..."
kubectl delete pvc data-redis-0

echo "Verifying that PVCs have been removed..."
sleep 10
kubectl get pvc