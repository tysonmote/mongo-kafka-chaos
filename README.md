# mongodb-kafka-chaos

This repo contains a basic MongoDB to Kafka pipeline using the
"Confluent-verified" [MongoDB Kafka Connector][connector]. It includes a
container that generates events with a monotonically-increasing integer, a
consumer that verifies that events are produced to Kafka exactly once and in
order, as well as a script to cause chaos by randomly killing containers.

[connector]: https://www.mongodb.com/docs/kafka-connector/current/?_ga=2.115834949.290014579.1649258771-1223676955.1643406626&_gac=1.261361151.1647454191.CjwKCAjwlcaRBhBYEiwAK341jSzBbJEryvLIhhyu9ZmZxujVI51zQ5uWrH38fVaOYXkW2Qnhf2zOaBoC9xIQAvD_BwE

I haven't played around with the Kafka REST proxy or the Schema Registry, but
you can uncomment their lines in `docker-compose.yml` to play with them.

MongoDB is pegged to 4.4, which is the version we run in production. You can
test upgrades (or downgrades) by updating the image tag in `docker-compose.yml`.

Kafka images are pegged to 7.4, which is the "Confluent Platform" version that
uses Kafka 3.4.0, the latest version of Kafka that AWS MSK supports.

## Running the pipeline

The reset script tears down any running containers and creates a fresh, running
test pipeline:

```
./reset.sh
```

You can tail logs for the `consumer` container to watch for errors:

```
docker-compose logs consumer -f
```

## Chaos

```
# Send SIGKILL to a random container every 15 seconds
./chaos.sh

# Send SIGTERM to a random MongoDB container every 10 seconds
./chaos -s SIGTERM -i 10 mongo1,mongo2,mongo3

# Send SIGKILL to kafka1 every 5 seconds
./chaos -i 5 kafka1
```

## Mongo ops

```
# Shell
docker-compose exec mongo1 mongosh
```

## Kafka ops

```
# List topics
docker-compose exec kafka1 kafka-topics --list --bootstrap-server localhost:9092

# Tail topic
docker-compose exec kafka1 kafka-console-consumer --topic chaos.events --bootstrap-server localhost:9092
```
