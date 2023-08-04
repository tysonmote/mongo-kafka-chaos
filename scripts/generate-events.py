from datetime import datetime

import pymongo

print("Connecting to MongoDB...", flush=True)

client = pymongo.MongoClient("mongodb://mongo1:27017/?replicaSet=rs&retryWrites=true&w=majority")
events = client.chaos.events

print("Creating TTL index...", flush=True)

try:
    events.create_index([("created_at", pymongo.ASCENDING)], expireAfterSeconds=60)
except pymongo.errors.OperationFailure:
    print("Index already exists", flush=True)

print("Generating events...", flush=True)

i = 0
while True:
    with client.start_session() as session:
        with session.start_transaction():
            requests = []
            now = datetime.utcnow()
            for _ in range(5):
                i += 1
                requests.append(pymongo.InsertOne({"created_at": now, "i": i}))
            events.bulk_write(requests, session=session)

    if i % 1000 == 0:
        print(f"Inserted {i} events", flush=True)
