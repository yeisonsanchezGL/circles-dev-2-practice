from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )


class ItemIn(_Base):
    sku: str
    name: str
    qty: int = Field(..., ge=1)
    unitPrice: Decimal = Field(..., alias="unitPrice")


class OrderIn(_Base):
    customerId: str
    items: list[ItemIn]
    couponCode: Optional[str] = None


class DiscountAppliedOut(_Base):
    code: str
    type: str
    amount: str


class OrderTotalsOut(_Base):
    subtotal: str
    discountsApplied: list[DiscountAppliedOut]
    discountTotal: str
    total: str


class OrderOut(OrderTotalsOut):
    id: str
    customerId: str
    items: list[dict[str, Any]]
    couponCode: Optional[str] = None
    createdAt: datetime

