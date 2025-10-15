from pymongo import MongoClient
import os

def get_collection():
    # Для локального тестирования используем MONGO_URI из env, по умолчанию localhost
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["mydatabase"]
    return db["users"]