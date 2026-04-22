# ORM Playground (Django + DRF + React)

This project helps learners practice Django ORM and SQL thinking through read-only APIs.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL
- Redis
- React (Vite)
- Docker Compose

## Phase Plan

- Phase 1: Project bootstrap, read-only API setup, seed sample data.
- Phase 2: Query practice endpoints (filtering, sorting, pagination).
- Phase 3: Guided ORM challenges and hints.
- Phase 4: Performance tuning (indexes, explain plans, caching).
- Phase 5: Auth, progress tracking, and deployment hardening.

## Run (Phase 1)

1. Copy env file:
   - `cp .env.example .env`
2. Start all services:
   - `docker compose up --build`
3. Open:
   - Backend API root: http://localhost:8000/api/
   - Frontend: http://localhost:5173/

## Current Constraints

- Only GET endpoints are exposed.
- No write APIs are available.
- DB modifications by API users are blocked by design.
