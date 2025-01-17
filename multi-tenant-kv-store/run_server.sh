#!/bin/bash

# Stop Redis server
echo "Stopping Redis server..."
sudo systemctl stop redis


# Wait for 10 seconds
echo "Waiting for 10 seconds..."
sleep 10

# Start Redis server
echo "Starting Redis server..."
redis-server &

# Wait to ensure Redis starts properly
sleep 5

# Navigate to the project directory
cd /home/adesoji/multi-tenant-kv-store || exit

# Activate virtual environment
echo "Activating virtual environment..."
source venv/venv/bin/activate

# Start Uvicorn server
echo "Starting Uvicorn server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &

# Start Huey worker
echo "Starting Huey consumer..."
python -m huey.bin.huey_consumer src.services.tasks.huey &
