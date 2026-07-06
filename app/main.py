from pathlib import Path
from time import perf_counter
import joblib

from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "incident_severity_model.joblib"

app = FastAPI(
    title="Enterprise AI Rollout",
    description="Week 1 prototype for AI Scaling and API Integration.",
    version="0.1.0"
)

class IncidentRequest(BaseModel):
    message: str = Field(..., min_length=5)

class PredictionResponse(BaseModel):
    severity: str
    model_version: str
    latency_ms: float

metrics = {
    "total_requests": 0,
    "errors": 0,
    "latencies_ms": []
}

def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

model = load_model()

def fallback_predict(message: str) -> str:
    text = message.lower()

    if any(word in text for word in ["timeout", "unavailable", "crash", "payment", "gateway"]):
        return "Critical"

    if any(word in text for word in ["error", "latency", "kafka", "disk", "500"]):
        return "High"

    if any(word in text for word in ["slow", "delay", "cache", "batch"]):
        return "Medium"

    return "Low"

@app.get("/")
def root():
    return {
        "message": "Enterprise AI Rollout API is running",
        "project": "AI Scaling and API Integration"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict-severity", response_model=PredictionResponse)
def predict_severity(request: IncidentRequest):
    start = perf_counter()
    metrics["total_requests"] += 1

    if model is not None:
        severity = model.predict([request.message])[0]
    else:
        severity = fallback_predict(request.message)

    latency_ms = round((perf_counter() - start) * 1000, 2)
    metrics["latencies_ms"].append(latency_ms)

    return PredictionResponse(
        severity=severity,
        model_version="v1",
        latency_ms=latency_ms
    )

@app.get("/metrics")
def get_metrics():
    latencies = metrics["latencies_ms"]

    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0

    return {
        "total_requests": metrics["total_requests"],
        "errors": metrics["errors"],
        "average_latency_ms": avg_latency,
        "latest_latencies_ms": latencies[-10:]
    }
