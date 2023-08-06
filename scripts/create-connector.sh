#!/bin/bash -ex

while true; do
  curl -X POST \
    -H "Content-Type: application/json" \
    --data '
      {
        "name": "chaos-source",
        "config": {
          "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
          "connection.uri": "mongodb://mongo1",
          "database": "chaos",
          "collection": "events"
        }
      }
    ' \
    http://localhost:8083/connectors -w "\n" \
    && break

  echo "Waiting for Kafka Connect to stand up..."
  sleep 5
done

curl -X GET http://localhost:8083/connectors
