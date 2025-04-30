from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_connection():
    return MongoClient(os.getenv("MONGO_URI"))

def get_collections():
    client = get_mongo_connection()
    db = client['ranking']
    return db['crypto'], db['history']
