from __future__ import annotations

from pydantic import BaseModel
import os


class Settings(BaseModel):
    mongo_uri: str = "mongodb://mongo:27017"
    mongo_db: str = "shop"


def get_settings() -> Settings:
    return Settings(
        mongo_uri=os.getenv("MONGO_URI", "mongodb://mongo:27017"),
        mongo_db=os.getenv("MONGO_DB", "shop"),
    )

