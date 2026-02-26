from decimal import Decimal

from app.domain.discounts import DiscountApplied, Item, _cap_discounts, calculate_totals


def test_bulk10_applies_for_qty_10_plus():
    totals = calculate_totals([Item(sku="A", name="x", qty=10, unit_price=Decimal("3.50"))])
    assert totals.subtotal == Decimal("35.00")
    assert len(totals.discounts_applied) == 1
    assert totals.discounts_applied[0].code == "BULK10"
    assert totals.discounts_applied[0].amount == Decimal("3.50")
    assert totals.total == Decimal("31.50")


def test_order5_applies_when_subtotal_ge_100():
    totals = calculate_totals([Item(sku="A", name="x", qty=1, unit_price=Decimal("100.00"))])
    codes = [d.code for d in totals.discounts_applied]
    assert "ORDER5" in codes
    assert totals.discount_total == Decimal("5.00")
    assert totals.total == Decimal("95.00")


def test_welcome15_capped_at_20():
    totals = calculate_totals(
        [Item(sku="A", name="x", qty=1, unit_price=Decimal("200.00"))], coupon_code="WELCOME15"
    )
    coupon = [d for d in totals.discounts_applied if d.code == "WELCOME15"][0]
    assert coupon.amount == Decimal("20.00")


def test_safety_cap_reduces_last_discount_to_fit():
    discounts = [
        DiscountApplied(code="BULK10", type="line", amount=Decimal("10.00")),
        DiscountApplied(code="ORDER5", type="order", amount=Decimal("5.00")),
        DiscountApplied(code="WELCOME15", type="coupon", amount=Decimal("20.00")),
    ]
    capped = _cap_discounts(discounts, cap=Decimal("30.00"))
    assert sum((d.amount for d in capped), Decimal("0")) == Decimal("30.00")
    assert capped[-1].amount == Decimal("15.00")

