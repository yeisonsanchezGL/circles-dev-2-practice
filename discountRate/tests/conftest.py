from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient


@pytest.fixture(scope="session")
def mongo_uri() -> str:
    return os.getenv("MONGO_URI", "mongodb://mongo:27017")


@pytest.fixture(scope="session")
def mongo_db() -> str:
    return os.getenv("MONGO_DB", "shop_test")


@pytest.fixture(scope="session")
def mongo_client(mongo_uri: str) -> MongoClient:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
    # Force connection early for clearer failures
    client.admin.command("ping")
    return client


@pytest.fixture()
def clean_orders(mongo_client: MongoClient, mongo_db: str):
    mongo_client[mongo_db]["orders"].delete_many({})
    yield
    mongo_client[mongo_db]["orders"].delete_many({})


@pytest.fixture()
def client(mongo_db: str, clean_orders):
    os.environ["MONGO_DB"] = mongo_db
    from app.main import create_app

    app = create_app()
    with TestClient(app) as c:
        yield c

