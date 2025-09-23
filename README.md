# Moshoflo – Real-Time Trade Dashboard

Moshoflo is a dashboard built with FastAPI, WebSockets, and React. It demonstrates trade streaming, visualization, and simple risk scoring using a lightweight PyTorch model trained on synthetic data. The project showcases real-time API integration, WebSocket handling, and CI pipelines with GitHub Actions.

---

## Demo

Visuals of the live dashboard:

### All Trades View
![All Trades](demo/demo-overview-1.png)

### 🟢 Low Risk Filter
![High Risk](demo/demo-overview-2.png)

### 🟠 Medium Risk Filter
![Medium Risk](demo/demo-overview-3.png)

### 🔴 High Risk Filter
![Low Risk](demo/demo-overview-4.png)


---

## 🔧 Features

- **Real-Time Streaming** via WebSockets  
- **ML-Powered Risk Classification** (PyTorch inference on synthetic data)  
- **API Architecture** with FastAPI  
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
| ML         | Python, PyTorch(inference), scikit-learn, joblib  |
| Frontend   | React, Vite                            |
| DevOps     | Docker, GitHub Actions, Flake8, Pytest |

---

## Project Structure

```
moshoflo/
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── db.py                # DB setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/              # API & WebSocket routes
│   └── Dockerfile
├── ai/
│   ├── predictor.py         # Inference logic
│   ├── train_model.py       # Model training script
│   └── *.pt, *.npy          # Generated model + encoder (created during training; not committed)
├── frontend/                # React + Vite frontend
└── .github/workflows/       # GitHub CI config
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

- [ ] Upgrade prototype classifier into a more robust ML service (e.g. TorchScript/ONNX)  
- [ ] Add Docker Compose support for full stack
- [ ] Improve frontend UI/UX for live trade tracking
- [ ] Persist trades and classifications in database (currently in-memory)
- [ ] Add unit tests for ML inference via `predictor.py`
- [ ] Log model prediction confidence scores (for future calibration work)
- [ ] Explore switching from joblib to TorchScript or ONNX for deployment
- [ ] (Stretch) Add batch classification API route for bulk trade analysis

---

## 👤 Author

**Mosorire Omisore** – 2025
Built as an AI infrastructure prototype.
