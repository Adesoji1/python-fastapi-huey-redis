#!/bin/bash


cd ~/Documents/cambsubmission/multi-tenant-kv-store/k8s || exit

echo "Applying Redis StatefulSet and Service..."
kubectl apply -f redis-statefulset.yaml
sleep 50
kubectl apply -f redis-service.yaml
sleep 50
echo "Applying FastAPI and Huey deployments..."
kubectl apply -f fastapi-deployment.yaml
sleep 50
kubectl apply -f huey-deployment.yaml
sleep 50

echo "Applying Grafana and Prometheus deployments..."
kubectl apply -f grafana-deployment.yaml
sleep 50
kubectl apply -f prometheus-deployment.yaml
sleep 50

echo "Verifying that all resources are starting..."
kubectl get pods
sleep 50
kubectl get deployments
sleep 20
kubectl get services
sleep 10


echo "Port forwarding for Prometheus on localhost:9090..."
kubectl port-forward svc/prometheus 9090:9090 &

echo "Port forwarding for Grafana on localhost:3000..."
kubectl port-forward svc/grafana 3000:3000 &

echo "Port forwarding for Locust on localhost:8089..."
kubectl port-forward service/locust 8089:8089 &


echo "Port forwarding for FastAPI on localhost:8000..."
kubectl port-forward svc/fastapi-service 8000:8000 &