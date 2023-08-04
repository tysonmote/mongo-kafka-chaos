#!/bin/sh -ex

docker-compose down --volumes

docker-compose up -d

docker-compose exec mongo1 bash -c "/scripts/bootstrap-mongo.sh"

echo "Waiting for Kafka Connect to stand up..."
sleep 10

docker-compose exec connect bash -c "/scripts/create-connector.sh"
