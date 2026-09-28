import json
import os
import sys

import pandas as pd
import pymongo
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URI") or os.getenv("MONGO_DB_URL")


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            if not MONGO_DB_URL:
                raise ValueError("MongoDB URL is missing. Set MONGODB_URI in your .env file.")

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=5000)
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]
            result = self.collection.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "network"
    collection_name = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(f"Fetched {len(records)} records")
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, collection_name)
    print(f"Inserted {no_of_records} records into MongoDB")

