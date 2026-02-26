from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from bson import ObjectId
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database


@dataclass
class OrderRepository:
    collection: Collection

    @classmethod
    def from_database(cls, db: Database) -> "OrderRepository":
        collection = db["orders"]
        repo = cls(collection=collection)
        repo.ensure_indexes()
        return repo

    def ensure_indexes(self) -> None:
        self.collection.create_index([("createdAt", ASCENDING)])
        self.collection.create_index([("customerId", ASCENDING)])

    def create(self, doc: dict[str, Any]) -> str:
        doc = {**doc, "createdAt": datetime.now(timezone.utc)}
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)

    def get(self, order_id: str) -> Optional[dict[str, Any]]:
        try:
            oid = ObjectId(order_id)
        except Exception:
            return None

        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return None

        doc["id"] = str(doc.pop("_id"))
        return doc

