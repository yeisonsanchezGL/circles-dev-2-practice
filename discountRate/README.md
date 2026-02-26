# discountRate

FastAPI service that calculates order totals with deterministic discount rules and persists orders in MongoDB.

## Requirements

- Docker + Docker Compose

## Run

1) Create env file:

```bash
cp .env.example .env
```

2) Start API + MongoDB (+ Mongo Express):

```bash
docker compose up --build
```

- API: `http://localhost:8000` (docs at `/docs`)
- API: `http://localhost:8002` (docs at `/docs`)
- Mongo Express: `http://localhost:8081`

## Run tests (inside container)

```bash
docker compose run --rm -e MONGO_DB=shop_test api pytest -q
```

## Sample curl

Preview (no persistence):

```bash
curl -sS -X POST "http://localhost:8002/orders/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "cust_123",
    "couponCode": "WELCOME15",
    "items": [
      {"sku": "A1", "name": "Widget", "qty": 10, "unitPrice": "3.50"},
      {"sku": "B2", "name": "Gadget", "qty": 2, "unitPrice": "50.00"}
    ]
  }'
```

Create (persist to MongoDB):

```bash
curl -sS -X POST "http://localhost:8002/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "cust_123",
    "couponCode": "WELCOME15",
    "items": [
      {"sku": "A1", "name": "Widget", "qty": 10, "unitPrice": "3.50"},
      {"sku": "B2", "name": "Gadget", "qty": 2, "unitPrice": "50.00"}
    ]
  }'
```

Get by id:

```bash
curl -sS "http://localhost:8002/orders/<id>"
```
