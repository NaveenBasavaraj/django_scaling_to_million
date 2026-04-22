# Phase 1 Learning Path (Build + Learn)

## Goal

Set up a full-stack, dockerized environment and understand how DRF exposes read-only ORM-backed data.

## What to Learn While Building

- Django project/app structure (`config` vs app modules)
- Models and relationships (`ForeignKey`, query ordering)
- DRF read-only viewsets and serializers
- Docker Compose service networking
- PostgreSQL as primary DB and Redis as infra dependency

## Hands-on Tasks

1. Start stack with `docker compose up --build`
2. Call API endpoints:
   - `/api/customers/`
   - `/api/categories/`
   - `/api/products/`
   - `/api/orders/`
3. Open DRF list endpoints and inspect JSON fields.
4. Try write verbs (POST/PUT/DELETE) to confirm they are blocked.
5. Visit React frontend and compare counts with API output.

## ORM Exercises (beginner)

1. List all products with their category names.
2. Find all orders for a single customer.
3. Get products with stock less than 50.
4. Get top 2 customers by order count.

## Exit Criteria for Phase 1

- Environment boots with one command.
- Seed data is available automatically.
- APIs are read-only.
- You can explain each model relationship.
