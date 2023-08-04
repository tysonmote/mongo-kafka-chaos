import orjson
import random

from kafka import KafkaConsumer
from _lib import IndexSet, RateTracker


def parse_index(msg):
    """
    Extract the MongoDB event index from a Kafka message containing a MongoDB
    change stream record.
    """

    payload = orjson.loads(msg.get("payload"))
    if payload is None:
        raise Exception(f"Payload is missing: {msg}")

    if payload.get("operationType") != "insert":
        return None

    document = payload.get("fullDocument")
    if document is None:
        raise Exception(f"Missing fullDocument: {payload}")

    event_i = document.get("i")
    if event_i is None:
        raise Exception(f"Missing event index: {document}")

    return event_i


def main():
    consumer = KafkaConsumer(
        "chaos.events",
         bootstrap_servers=["kafka:9092"],
         group_id="consumer-0",
         auto_commit_interval_ms=1000,
         value_deserializer=lambda b: orjson.loads(b.decode("utf-8"))
     )

    rate = RateTracker(label="Events consumed", interval=100000)

    seen = IndexSet()
    prev = None

    print("Consuming events...", flush=True)

    for msg in consumer:
        try:
            event_i = parse_index(msg.value)
        except Exception as e:
            print(f"ERROR: {e}", flush=True)
            continue

        if event_i is None:
            continue

        rate.tick()

        if event_i == 0 or prev is None:
            print(f"Got first event, resetting state", flush=True)
            prev = event_i
            index_set = IndexSet()
            index_set.add(event_i)
            continue

        # Ensure monotonically increasing event index.
        if event_i > prev + 1:
            print(f"ERROR: Missing events between {prev} and {event_i}", flush=True)
        elif event_i < prev:
            print(f"ERROR: Got event {event_i} after {prev} (out of order)", flush=True)

        if event_i in seen:
            print(f"ERROR: Duplicate event {event_i}", flush=True)
        else:
            seen.add(event_i)

        prev = event_i


if __name__ == "__main__":
    main()
