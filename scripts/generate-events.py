from datetime import datetime

import pymongo
from _lib import RateTracker

def main():
    print("Connecting to MongoDB...", flush=True)
    client = pymongo.MongoClient("mongodb://mongo1:27017/?replicaSet=rs&retryWrites=true&w=majority")
    events = client.chaos.events

    try:
        print("Creating TTL index...", flush=True)
        events.create_index([("created_at", pymongo.ASCENDING)], expireAfterSeconds=120)
    except pymongo.errors.OperationFailure:
        print("Index already exists", flush=True)

    rate = RateTracker(label="Events generated", interval=10000)
    i = 0

    print("Generating events...", flush=True)
    while True:
        with client.start_session() as session:
            with session.start_transaction():
                requests = []
                now = datetime.utcnow()
                for _ in range(5):
                    rate.tick()
                    requests.append(pymongo.InsertOne({"created_at": now, "i": i}))
                    i += 1
                events.bulk_write(requests, session=session)


if __name__ == "__main__":
    main()

