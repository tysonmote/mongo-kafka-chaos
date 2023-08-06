#!/bin/sh -e

echo "Cleaning up..."
docker-compose down --volumes

echo "Starting up..."
docker-compose up -d

echo "Bootstrapping MongoDB replica set..."
docker-compose exec mongo1 bash -c "/scripts/bootstrap-mongo.sh"

echo "Creating Kafka Connect connector..."
docker-compose exec connect bash -c "/scripts/create-connector.sh"
