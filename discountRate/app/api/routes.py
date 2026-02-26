from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.main_deps import get_order_service
from app.schemas.orders import OrderIn, OrderOut, OrderTotalsOut
from app.services.order_service import OrderService

router = APIRouter()


@router.post("/orders/preview", response_model=OrderTotalsOut)
def preview_order(order_in: OrderIn, svc: OrderService = Depends(get_order_service)):
    return svc.preview(order_in)


@router.post("/orders", response_model=OrderOut)
def create_order(order_in: OrderIn, svc: OrderService = Depends(get_order_service)):
    return svc.create(order_in)


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str, svc: OrderService = Depends(get_order_service)):
    if not svc.repo:
        raise HTTPException(status_code=500, detail="Repository not configured")

    doc = svc.repo.get(order_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")
    return doc

