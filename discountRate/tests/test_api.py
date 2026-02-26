def test_preview_calculates_totals(client):
    r = client.post(
        "/orders/preview",
        json={
            "customerId": "cust_1",
            "couponCode": "WELCOME15",
            "items": [
                {"sku": "A1", "name": "Widget", "qty": 10, "unitPrice": "3.50"},
                {"sku": "B2", "name": "Gadget", "qty": 2, "unitPrice": "50.00"},
            ],
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["subtotal"] == "135.00"
    assert body["discountTotal"] == "28.50"
    assert body["total"] == "106.50"
    assert [d["code"] for d in body["discountsApplied"]] == ["BULK10", "ORDER5", "WELCOME15"]


def test_create_and_get_round_trip(client):
    r = client.post(
        "/orders",
        json={
            "customerId": "cust_2",
            "items": [{"sku": "A1", "name": "Widget", "qty": 1, "unitPrice": "100.00"}],
        },
    )
    assert r.status_code == 200, r.text
    created = r.json()
    assert "id" in created
    assert created["customerId"] == "cust_2"
    assert created["subtotal"] == "100.00"
    assert created["discountTotal"] == "5.00"
    assert created["total"] == "95.00"

    r2 = client.get(f"/orders/{created['id']}")
    assert r2.status_code == 200, r2.text
    fetched = r2.json()
    assert fetched["id"] == created["id"]
    assert fetched["total"] == "95.00"

