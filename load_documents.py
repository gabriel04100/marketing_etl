from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
import logging
import json



def insert_documents__into_mongodb(data, MONGO_URL,db_name, collection_name):
    """Insert data into MongoDB collection."""
    try:
        # Connect to MongoDB
        with MongoClient(MONGO_URL) as client:
            db = client[db_name]
            collection = db[collection_name]

            # Insert JSON data into the collection
            if data:
                result = collection.insert_many(data)
                logging.info("Inserted {} documents into '{}.{}'".format(
                    len(result.inserted_ids), db_name, collection_name
                    ))
            else:
                logging.warning("No data to insert into '{}.{}'".format(
                    db_name, collection_name
                ))

    except errors.ConnectionError as ce:
        logging.error(f"Connection error: {ce}")
        raise
    except errors.PyMongoError as e:
        logging.error(f"MongoDB insertion error: {e}")
        raise
    finally:
        client.close()
        logging.info("MongoDB connection closed.")


def insert_items_batch(data_batch, MONGO_URL, db_name):
    #users transactions  product_reviews  products
    db_collections = {"users":data_batch.get("users"),
                      "transactions":data_batch.get("transactions"),
                      "product_reviews":data_batch.get("product_reviews"),
                      "products":data_batch.get("products")}

    for collection_key in db_collections.keys():
        insert_documents__into_mongodb(data=db_collections[collection_key],
                                       MONGO_URL=MONGO_URL,
                                       db_name=db_name,
                                       collection_name=collection_key)




logging.basicConfig(filename="./logs/insert_batch.log")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file located in the same directory
load_dotenv(os.path.join(script_dir, '.env'))

MONGO_URL = os.getenv("MONGO_URL")
db_name="product_transactions"

with open("./data/initial_batch_products.json") as json_batch:
    batch = json.load(json_batch)

print(batch)

try:
    insert_items_batch(batch, MONGO_URL=MONGO_URL, db_name=db_name)

except Exception as e:
    print("error trying to insert files")


    

