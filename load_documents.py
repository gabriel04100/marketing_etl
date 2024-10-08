from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
import logging


logging.basicConfig(filename="./insert_batch.log")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file located in the same directory
load_dotenv(os.path.join(script_dir, '.env'))

MONGO_URL = os.getenv("MONGO_URL")


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


def insert_items_batch(data):
    #users transactions  product_reviews  products
    users = data["users"]
    transactions = data["transactions"]
    product_review = data["product_reviews"]
    products = data["products"]