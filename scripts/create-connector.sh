#!/bin/bash -ex

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
    http://localhost:8083/connectors -w "\n"

curl -X GET http://localhost:8083/connectors
