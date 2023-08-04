#!/bin/bash

pip install kafka-python orjson --disable-pip-version-check

while true; do
  python /scripts/consume-events.py
  echo "Exited with code $?, restarting in 1 second..."
  sleep 1
done

