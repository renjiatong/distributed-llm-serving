# 🚀 LLM Serving Backend (FastAPI + OpenAI + SSE + Prometheus + Grafana)

A modular, production-grade backend designed to serve LLM chat responses with
streaming support, observability, and modern backend engineering practices.

This project follows a step-by-step roadmap toward a full LLM serving stack
(compatible with vLLM in future steps).  
Currently, it implements:

- FastAPI service gateway  
- Chat API (normal + streaming / SSE)  
- Modular backend architecture  
- Frontend chat UI for testing  
- JSON logging + request tracing  
- Prometheus metrics instrumentation  
- Grafana dashboards connected to Prometheus  

---

## ✨ Features Completed

### ✅ **1. FastAPI Backend**
- Project structured using `routers/`, `services/`, `schemas/`, `utils/`
- `/health` endpoint  
- `/chat` endpoint (sync reply)
- `/chat/stream` endpoint (Server-Sent Events streaming)

### 📡 **2. Streaming Chat (SSE)**
- Real-time token streaming (mocked via OpenAI streaming API)
- Frontend displays assistant replies character-by-character (ChatGPT-style)

### 🧩 **3. Modular Service Architecture**
- `chat_service.py` handles model calls
- Ready for a single-line engine swap from OpenAI → vLLM later
- Clean separation of concerns for maintainability

### 🪵 **4. Observability: Logging + Tracing**
- Structured JSON logs  
- Trace ID generated per request  
- Logs include:
  - trace_id  
  - method  
  - path  
  - latency  
  - message  

### 📈 **5. Prometheus Metrics Integration**
- `/metrics` endpoint exposing:
  - `http_requests_total`
  - `http_request_duration_ms` (Histogram)
- Request count + latency instrumented via middleware

### 📊 **6. Grafana Dashboards**
Using Docker Compose:

- Prometheus running on port **9090**
- Grafana running on port **3000**
- Dashboards include:
  - QPS (Requests per second)
  - Latency (p50 / p90 / p99)
  - Requests by path
  - Histogram distributions

---

## 🧪 Frontend Chat UI

A minimal HTML/JS frontend for testing:

- Input box to send messages
- Message history (user + assistant)
- SSE support for streaming responses
- Trace ID displayed with assistant replies

This UI allows quick testing without Postman/CLI.

---

## 🐳 Running Prometheus + Grafana

### Start monitoring stack:

```bash
docker compose up -d

URLs:

Grafana: http://localhost:3000

Prometheus: http://localhost:9090

FastAPI docs: http://localhost:8000/docs

Metrics endpoint: http://localhost:8000/metrics
