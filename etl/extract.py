from pymongo import MongoClient, errors
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(
    filename="./logs/extract_log.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

MONGO_URL = os.getenv("MONGODB_URI")

def extract_collection(mongo_url, db, collection, filter=None, projection=None):
        try:
            with MongoClient(mongo_url) as client:
                db=client[db]
                collection=db[collection]
                cursor = collection.find(filter, projection)
                logging.info("extract sucessfull")
                return list(cursor)
        except errors.PyMongoError as e:
            logging.error(f"extract failed {e}")
            return {}
        
db="product_transactions"
collection="users"
print(extract_collection(MONGO_URL,db,collection))