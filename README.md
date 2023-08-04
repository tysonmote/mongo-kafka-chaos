This repo contains a basic MongoDB -> Kafka pipeline using the
"Confluent-verified" [MongoDB Kafka Connector][connector]. It includes a
container that generates events with a monotonically-increasing integer and a
consumer that verifies that events are produced to Kafka exactly once in order.

[connector]: https://www.mongodb.com/docs/kafka-connector/current/?_ga=2.115834949.290014579.1649258771-1223676955.1643406626&_gac=1.261361151.1647454191.CjwKCAjwlcaRBhBYEiwAK341jSzBbJEryvLIhhyu9ZmZxujVI51zQ5uWrH38fVaOYXkW2Qnhf2zOaBoC9xIQAvD_BwE

## Setup / reset

The reset script tears down any running containers and creates a fresh, running
test pipeline.

```
./reset.sh
```

## Mongo ops

```
# Shell
docker-compose exec mongo1 mongosh
```

## Kafka ops

```
# List topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Tail topic
docker-compose exec kafka kafka-console-consumer --topic chaos.events --bootstrap-server localhost:9092
```
