import heapq
import orjson

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "chaos.events",
     bootstrap_servers=["kafka:9092"],
     group_id="consumer-0"
 )

# Payload:
#
# {
#   "_id": {
#     "_data": "8264CC7A0D0000015B2B022C0100296E5A1004B249DE6678774515B56291AA9809FEA646645F6964006464CC7A0DB5E1075F0F96A3EC0004"
#   },
#   "operationType": "insert",
#   "clusterTime": {
#     "$timestamp": {
#       "t": 1691122189,
#       "i": 347
#     }
#   },
#   "fullDocument": {
#     "_id": {
#       "$oid": "64cc7a0db5e1075f0f96a3ec"
#     },
#     "createdAt": {
#       "$date": 1691122189483
#     },
#     "n": 38540,
#     "i": 192701
#   },
#   "ns": {
#     "db": "chaos",
#     "coll": "events"
#   },
#   "documentKey": {
#     "_id": {
#       "$oid": "64cc7a0db5e1075f0f96a3ec"
#     }
#   }
# }

prev = None
recent_set = set()
recent_heap = []
i = 0

print("Consuming events...", flush=True)

for msg in consumer:
    message = orjson.loads(msg.value)
    if message is None:
        print("ERROR: Got None message", flush=True)
        continue

    payload = orjson.loads(message.get("payload"))
    if payload is None:
        print(f"ERROR: Payload is missing: {message}", flush=True)
        continue

    if payload.get("operationType") != "insert":
        continue

    document = payload.get("fullDocument")
    if document is None:
        print(f"ERROR: Missing fullDocument: {message}", flush=True)
        continue

    event_i = document.get("i")
    if event_i is None:
        print(f"ERROR: Missing event index: {document}", flush=True)
        continue

    if prev is not None:
        if event_i - prev != 1:
            print(f"ERROR: Missing events between {prev} and {event_i}", flush=True)
        if event_i < prev:
            print(f"ERROR: Got event {event_i} after {prev}", flush=True)

    if event_i in recent_set:
        print(f"ERROR: Duplicate event {event_i}", flush=True)
    else:
        recent_set.add(event_i)
        heapq.heappush(recent_heap, event_i)
        if len(recent_heap) > 100000:
            recent_set.remove(heapq.heappop(recent_heap))

    prev = event_i

    i += 1
    if i % 1000 == 0:
        print(f"Consumed {i} events", flush=True)

