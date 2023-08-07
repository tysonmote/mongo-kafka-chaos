#!/bin/sh -e

while true; do
  mongo --eval 'db' && break
  echo "Waiting for MongoDB to stand up..."
  sleep 2
done

echo "Initializing replica set..."
echo 'rs.initiate({_id: "rs", version: 1, members: [ { _id: 0, host : "mongo1:27017" }, { _id: 1, host : "mongo2:27017" }, { _id: 2, host : "mongo3:27017" } ] })' | mongosh
echo "Replica set initialized!"
