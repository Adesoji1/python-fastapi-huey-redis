#!/bin/bash

cd /home/adesoji || exit

echo "Stopping Redis server..."
sudo systemctl stop redis || echo "Failed to stop Redis using systemctl."

echo "Waiting for 5 seconds..."
sleep 5

echo "Stopping Uvicorn server..."
pkill -f "uvicorn src.main:app" || {
  echo "pkill failed, attempting to kill manually..."
  pgrep -f "uvicorn src.main:app" | xargs kill -9
}

echo "Stopping Huey consumer..."
pkill -f "python -m huey.bin.huey_consumer" || {
  echo "pkill failed, attempting to kill manually..."
  pgrep -f "python -m huey.bin.huey_consumer" | xargs kill -9
}

echo "All services have been stopped."
