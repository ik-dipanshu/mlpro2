import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("MONGODB_URI is not set in the environment or .env file.")

client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
except Exception as e:
    raise RuntimeError(f"The following error occurred: {e}") from e
finally:
    client.close()