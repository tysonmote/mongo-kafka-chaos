import pymongo

print("Connecting to MongoDB...", flush=True)

client = pymongo.MongoClient("mongodb://mongo1:27017/?replicaSet=rs&retryWrites=true&w=majority")
db = client.chaos

print("Creating capped events collection...", flush=True)

db.command("create", "events", capped=True, size=512000000, max=100000)

print("Generating events...", flush=True)

i = 0
while True:
    with client.start_session() as session:
        for _ in range(5):
            i += 1
            db.events.insert_one({"i": i}, session=session)

    if i % 1000 == 0:
        print(f"Inserted {i} events", flush=True)
