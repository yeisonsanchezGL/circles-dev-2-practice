from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.domain.discounts import Item, calculate_totals
from app.repositories.mongo_order_repository import OrderRepository
from app.schemas.orders import OrderIn
from app.utils.money import money_str


@dataclass
class OrderService:
    repo: Optional[OrderRepository] = None

    def _to_domain_items(self, order_in: OrderIn) -> list[Item]:
        return [
            Item(
                sku=i.sku,
                name=i.name,
                qty=i.qty,
                unit_price=i.unitPrice,
            )
            for i in order_in.items
        ]

    def preview(self, order_in: OrderIn) -> dict[str, Any]:
        totals = calculate_totals(self._to_domain_items(order_in), order_in.couponCode)
        return {
            "subtotal": money_str(totals.subtotal),
            "discountsApplied": [
                {"code": d.code, "type": d.type, "amount": money_str(d.amount)}
                for d in totals.discounts_applied
                if d.amount > 0
            ],
            "discountTotal": money_str(totals.discount_total),
            "total": money_str(totals.total),
        }

    def create(self, order_in: OrderIn) -> dict[str, Any]:
        if not self.repo:
            raise RuntimeError("Repository not configured")

        preview = self.preview(order_in)
        doc: dict[str, Any] = {
            "customerId": order_in.customerId,
            "couponCode": order_in.couponCode,
            "items": [
                {
                    "sku": i.sku,
                    "name": i.name,
                    "qty": i.qty,
                    "unitPrice": money_str(i.unitPrice),
                }
                for i in order_in.items
            ],
            **preview,
        }

        order_id = self.repo.create(doc)
        saved = self.repo.get(order_id)
        if not saved:
            raise RuntimeError("Order was not found after insert")
        return saved

