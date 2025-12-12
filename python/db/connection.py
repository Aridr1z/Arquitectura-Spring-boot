import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def get_database():
    """Create a MongoClient using environment variables and return the database."""
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "27017")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASS", "root")
    database_name = os.getenv("DB_NAME", "ecommerce")

    user_enc = quote_plus(user)
    password_enc = quote_plus(password)

    uri = f"mongodb://{user_enc}:{password_enc}@{host}:{port}/{database_name}?authSource=admin"
    client = MongoClient(uri)
    return client[database_name]
