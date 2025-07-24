# Moshoflo – Real-Time Trade Intelligence Dashboard

**Moshoflo** is a real-time financial trade monitoring and classification platform built with FastAPI, WebSockets, and React. It simulates the infrastructure required for streaming and visualizing financial trades in real time — complete with ML-driven risk scoring and live filtering.

---

## Demo

Visuals of the live dashboard in action:

### All Trades View
![All Trades](demo/demo-overview-1.png)

### 🔴 High Risk Filter
![High Risk](demo/demo-overview-2.png)

### 🟠 Medium Risk Filter
![Medium Risk](demo/demo-overview-3.png)

### 🟢 Low Risk Filter
![Low Risk](demo/demo-overview-4.png)


---

## 🔧 Features

- **Real-Time Streaming** via WebSockets  
- **ML-Powered Risk Classification** (using joblib model)  
- **API-First Architecture** with FastAPI  
- **Frontend Dashboard** built with React + Vite  
- **Docker-Compatible Backend** (Dockerfile included)  
- **CI Pipeline** with GitHub Actions  
- **Code Quality Tools** – Flake8 + Pytest  

---

## Tech Stack

| Layer       | Tools                                |
|------------|----------------------------------------|
| Backend    | FastAPI, SQLAlchemy, PostgreSQL        |
| Realtime   | WebSockets                             |
| ML         | Python, scikit-learn, joblib           |
| Frontend   | React, Vite                            |
| DevOps     | Docker, GitHub Actions, Flake8, Pytest |

---

## Project Structure

```
moshoflo/
├── backend/                # FastAPI backend
│   ├── main.py             # Entrypoint
│   ├── db.py               # DB connection
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── routes/             # API & WebSocket routes
│   └── Dockerfile
├── ai/                     # ML logic
│   ├── predictor.py
│   ├── train_model.py
│   └── *.joblib
├── frontend/               # React + Vite UI
└── .github/workflows/      # CI pipeline config
```

---

## Getting Started

### Backend Setup

```
cd backend
python -m venv .venv
source .venv/bin/activate     # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## Environment Configuration

Use the provided `.env.example` to configure your environment:

```bash
cp .env.example backend/.env
cp .env.example frontend/.env
```

**.env.example**
```
# Backend
DATABASE_URL=postgresql://admin:admin@localhost:5432/moshoflo

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/trades
```

---

## API Reference

### REST Endpoints

- `GET /trades/` – Retrieve all trades  
- `POST /trades/` – Submit a new trade

**Sample POST Body**
```
{
  "symbol": "TSLA",
  "price": 300.5,
  "volume": 150,
  "side": "BUY",
  "exchange": "NASDAQ",
  "currency": "USD"
}
```

### WebSocket Endpoint

```
ws://localhost:8000/ws/trades
```

- Sends JSON payloads in real-time on trade creation

---

## 🚧 Planned Enhancements

- [ ] Integrate production-grade ML classification endpoint  
- [ ] Add Docker Compose to orchestrate full stack locally  
- [ ] Enable persistent PostgreSQL volumes in dev  
- [ ] Polish dashboard UI/UX (live filters, responsive layout)  
- [ ] Track trade analytics with metrics (Prometheus / custom)

---

## 👤 Author

**Mosorire Omisore** – 2025