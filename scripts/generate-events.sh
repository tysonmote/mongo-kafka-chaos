#!/bin/bash -e

pip install pymongo --disable-pip-version-check

while true; do
  python /scripts/generate-events.py
  echo "Exited with code $?, restarting in 1 second..."
  sleep 1
done

