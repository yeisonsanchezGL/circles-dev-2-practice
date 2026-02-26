from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.mongo import get_database, get_mongo_client
from app.repositories.mongo_order_repository import OrderRepository
from app.services.order_service import OrderService


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = get_settings()
        client = get_mongo_client(settings.mongo_uri)
        db = get_database(client, settings.mongo_db)
        repo = OrderRepository.from_database(db)
        app.state.mongo_client = client
        app.state.order_service = OrderService(repo=repo)
        try:
            yield
        finally:
            client.close()

    app = FastAPI(title="Order Totals API", version="1.0.0", lifespan=lifespan)
    app.include_router(router)

    return app


app = create_app()

