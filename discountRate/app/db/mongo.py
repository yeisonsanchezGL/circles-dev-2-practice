from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database


def get_mongo_client(mongo_uri: str) -> MongoClient:
    return MongoClient(mongo_uri)


def get_database(client: MongoClient, db_name: str) -> Database:
    return client[db_name]

