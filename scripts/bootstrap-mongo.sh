#!/bin/sh -e

echo "Installing mongosh..."
apt-get update
apt-get install wget
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
apt-get install -y mongodb-mongosh
echo "mongosh installed!"

echo "Initializing replica set..."
echo 'rs.initiate({_id: "rs", version: 1, members: [ { _id: 0, host : "mongo1:27017" }, { _id: 1, host : "mongo2:27017" }, { _id: 2, host : "mongo3:27017" }, ] })' | mongosh
echo "Replica set initialized!"
