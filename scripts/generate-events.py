from datetime import datetime
from time import sleep

import pymongo
from pymongo.errors import OperationFailure
from _lib import RateTracker

def main():
    print("Connecting to MongoDB...", flush=True)
    client = pymongo.MongoClient("mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs&retryWrites=true&w=majority")
    events = client.chaos.events

    try:
        print("Creating TTL index...", flush=True)
        events.create_index([("created_at", pymongo.ASCENDING)], expireAfterSeconds=120)
    except OperationFailure:
        print("Index already exists", flush=True)

    rate = RateTracker(label="Events generated")
    i = 0

    print("Generating events...", flush=True)
    while True:
        n = 5
        base_i = i
        try:
            with client.start_session() as session:
                with session.start_transaction():
                    now = datetime.utcnow()
                    for ii in range(n):
                        events.insert_one({
                            "created_at": now,
                            "i": base_i+ii
                        }, session=session)
            rate.tick(n)
            i = base_i + n
        except Exception as e:
            print(f"{e}", flush=True)
            print("Retrying in 1 second...", flush=True)
            sleep(1)
            continue


if __name__ == "__main__":
    main()

