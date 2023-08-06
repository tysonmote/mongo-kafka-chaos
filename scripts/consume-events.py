import orjson

from kafka import KafkaConsumer
from _lib import IndexSet, RateTracker


def parse_index(msg):
    """
    Extract the MongoDB event index from a Kafka message containing a MongoDB
    change stream record.
    """

    try:
        msg = orjson.loads(msg.decode("utf-8"))
    except Exception as e:
        raise Exception(f"Failed to parse message as JSON: {e}")

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
         bootstrap_servers=["kafka1:9092", "kafka2:9092", "kafka3:9092"],
         group_id="consumer-0",
         auto_commit_interval_ms=1000,
     )

    rate = RateTracker(label="Events consumed")

    seen = IndexSet()
    prev = None

    print("Consuming events...", flush=True)

    for msg in consumer:
        # Skip if first byte of body is null. I have no idea where these
        # messages are coming from; they started appearing only after upgrading
        # Kafka Connect 3.3.x (and 3.4.x). 3.2.x does not produce these
        # messages.
        if msg.value[0] == 0:
            continue

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
