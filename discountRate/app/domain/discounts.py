from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Optional


@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    qty: int
    unit_price: Decimal


@dataclass
class DiscountApplied:
    code: str
    type: str  # line | order | coupon
    amount: Decimal


@dataclass(frozen=True)
class Totals:
    subtotal: Decimal
    discounts_applied: list[DiscountApplied]
    discount_total: Decimal
    total: Decimal


def _cap_discounts(discounts: list[DiscountApplied], cap: Decimal) -> list[DiscountApplied]:
    if cap <= Decimal("0"):
        for d in discounts:
            d.amount = Decimal("0")
        return discounts

    def current_total() -> Decimal:
        return sum((d.amount for d in discounts), Decimal("0"))

    over = current_total() - cap
    if over <= Decimal("0"):
        return discounts

    # Reduce from the last applied discount backwards until within cap.
    for d in reversed(discounts):
        if over <= Decimal("0"):
            break
        reducible = min(d.amount, over)
        d.amount -= reducible
        over -= reducible

    return discounts


def calculate_totals(items: Iterable[Item], coupon_code: Optional[str] = None) -> Totals:
    items_list = list(items)
    subtotal = sum((Decimal(i.qty) * i.unit_price for i in items_list), Decimal("0"))

    discounts: list[DiscountApplied] = []

    # 1) Line discount BULK10
    for i in items_list:
        if i.qty >= 10:
            line_total = Decimal(i.qty) * i.unit_price
            discounts.append(
                DiscountApplied(code="BULK10", type="line", amount=line_total * Decimal("0.10"))
            )

    # 2) Order discount ORDER5
    if subtotal >= Decimal("100"):
        discounts.append(DiscountApplied(code="ORDER5", type="order", amount=Decimal("5.00")))

    # 3) Coupon discount WELCOME15
    if coupon_code == "WELCOME15":
        coupon_amount = subtotal * Decimal("0.15")
        if coupon_amount > Decimal("20.00"):
            coupon_amount = Decimal("20.00")
        discounts.append(DiscountApplied(code="WELCOME15", type="coupon", amount=coupon_amount))

    # 4) Safety cap
    cap = subtotal * Decimal("0.30")
    discounts = _cap_discounts(discounts, cap)

    discount_total = sum((d.amount for d in discounts), Decimal("0"))
    if discount_total < Decimal("0"):
        discount_total = Decimal("0")

    total = subtotal - discount_total
    if total < Decimal("0"):
        total = Decimal("0")

    return Totals(
        subtotal=subtotal,
        discounts_applied=discounts,
        discount_total=discount_total,
        total=total,
    )

