# Moshoflo — Real-Time Trade Dashboard

A real-time trade monitoring dashboard built with **FastAPI, PostgreSQL, WebSockets, and React**.

Trades are persisted in PostgreSQL and streamed to connected clients via WebSockets, separating initial state retrieval (REST) from incremental updates (push) to reduce latency and backend load.

![Dashboard](demo/Dashboard.png)

---

## Key Features

- **Real-time push updates** — new trades are broadcast to all connected clients via WebSockets
- **Hybrid REST + WebSocket architecture** — initial state via REST, incremental updates via push
- **PostgreSQL persistence** using SQLAlchemy models
- **Dynamic risk classification** (ML inference with heuristic fallback)
- **Docker Compose** for reproducible local environments
- **CI via GitHub Actions** (linting + backend tests)
- **Internal CLI** for database seeding and cleanup

---

## Architecture Overview

### Frontend (React + Vite)

- Fetches initial trade set from `GET /trades`
- Opens persistent WebSocket connection to `/ws/trades`
- Applies incremental updates in-memory using `trade_id` upsert logic
- Computes UI summaries and charts client-side

### Backend (FastAPI)

- `POST /trades`
  - Persists trade in PostgreSQL
  - Computes risk classification
  - Broadcasts the created trade event to all connected WebSocket clients

- `GET /trades`
  - Returns stored trades
  - Includes computed `risk_label` field

- Automatic table creation on startup (Docker-safe)

### Database (PostgreSQL)

- Stores trade records as the source of truth
- `risk_label` is computed at request time (not persisted in current version)

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy

### Database
- PostgreSQL

### Realtime
- Native WebSockets (FastAPI)

### Frontend
- React (Vite)
- Recharts (data visualization)

### Tooling
- Docker & Docker Compose
- GitHub Actions (CI)
- Internal CLI (database operations)

---

## Getting Started

### Run with Docker (Recommended)

```bash
docker compose up --build
```

Services:

- Frontend → http://localhost:3000
- Backend → http://localhost:8000
- WebSocket → ws://localhost:8000/ws/trades

---

### Run Locally (Without Docker)

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Set environment variable:

```bash
export DATABASE_URL="postgresql://admin:admin@localhost:5432/moshoflo"
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

### `GET /trades`

Returns stored trades with computed `risk_label`.

### `POST /trades`

Creates a trade, persists it, and broadcasts it to connected WebSocket clients.

### `WS /ws/trades`

Streams trade events in JSON format after successful trade creation.

---

## Risk Classification

Risk is determined using:

- A lightweight ML inference module (when dependencies are available)
- A deterministic heuristic fallback for environments without ML support

The fallback mechanism ensures the system remains operational in environments where ML dependencies are unavailable (e.g., CI pipelines).

---

## CLI (Database Operations)

Run inside Docker container:

Clear all trades:

```bash
docker compose exec backend python -m backend.cli clear
```

Seed trades:

```bash
docker compose exec backend python -m backend.cli seed --n 50
```

---

## Tests

Run backend tests:

```bash
cd backend
pytest
```

---

## Known Limitations

- CORS is permissive (development scope)
- No authentication or rate limiting (demo scope)
- Risk is computed dynamically and not persisted
- No pagination on trade queries (current version)

---

## Design Decisions

- WebSockets were chosen over polling to reduce latency and unnecessary API traffic.
- Risk classification is computed dynamically to decouple inference logic from persistence and allow rapid iteration before introducing migrations.
- Docker Compose is used to ensure reproducible local environments.

---

## Roadmap

- Introduce pagination & ordering for large trade sets
- Introduce database migrations (Alembic)
- Persist risk metadata (`risk_tier`, `risk_score`, `source`) using migrations
- Add ingestion simulation service for live trade generation
- Improve WebSocket reconnection handling
- Add structured logging and health checks
