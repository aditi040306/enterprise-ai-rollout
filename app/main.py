from pathlib import Path
from time import perf_counter
from typing import Optional, Dict
import random
import joblib

from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "models"

app = FastAPI(
    title="Enterprise AI Rollout",
    description="Week 2 prototype for AI Scaling, API Integration, Model Versioning, Shadow Deployment, and Canary Rollout.",
    version="0.2.0"
)


class IncidentRequest(BaseModel):
    message: str = Field(..., min_length=5)


class PredictionResponse(BaseModel):
    severity: str
    confidence: float
    model_version: str
    rollout_mode: str
    latency_ms: float
    shadow_prediction: Optional[Dict] = None


class RolloutConfig(BaseModel):
    active_model: str = Field("v1", pattern="^(v1|v2)$")
    shadow_enabled: bool = False
    canary_percent: int = Field(0, ge=0, le=100)


metrics = {
    "total_requests": 0,
    "errors": 0,
    "model_v1_requests": 0,
    "model_v2_requests": 0,
    "shadow_evaluations": 0,
    "shadow_disagreements": 0,
    "latencies_ms": []
}

rollout_config = {
    "active_model": "v1",
    "shadow_enabled": False,
    "canary_percent": 0
}


def load_model(version: str):
    model_path = MODEL_DIR / f"incident_severity_{version}.joblib"
    if model_path.exists():
        return joblib.load(model_path)
    return None


models = {
    "v1": load_model("v1"),
    "v2": load_model("v2")
}


def fallback_predict(message: str):
    text = message.lower()

    if any(word in text for word in ["timeout", "unavailable", "crash", "payment", "gateway"]):
        return "Critical", 0.70

    if any(word in text for word in ["error", "latency", "kafka", "disk", "500"]):
        return "High", 0.65

    if any(word in text for word in ["slow", "delay", "cache", "batch"]):
        return "Medium", 0.60

    return "Low", 0.55


def predict_with_model(message: str, version: str):
    model = models.get(version)

    if model is None:
        return fallback_predict(message)

    severity = model.predict([message])[0]
    confidence = 0.80

    try:
        probabilities = model.predict_proba([message])[0]
        confidence = round(float(max(probabilities)), 4)
    except Exception:
        confidence = 0.80

    return severity, confidence


def choose_model_version():
    canary_percent = rollout_config["canary_percent"]

    if canary_percent > 0:
        random_number = random.randint(1, 100)
        if random_number <= canary_percent:
            return "v2", "canary"

    return rollout_config["active_model"], "active"


def record_latency(latency_ms: float):
    metrics["latencies_ms"].append(latency_ms)

    if len(metrics["latencies_ms"]) > 1000:
        metrics["latencies_ms"] = metrics["latencies_ms"][-1000:]


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Rollout API is running",
        "project": "AI Scaling and API Integration",
        "week": "Week 2"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "loaded_models": {
            "v1": models["v1"] is not None,
            "v2": models["v2"] is not None
        },
        "current_rollout_config": rollout_config
    }


@app.post("/predict-severity", response_model=PredictionResponse)
def predict_severity(request: IncidentRequest):
    start = perf_counter()
    metrics["total_requests"] += 1

    try:
        selected_model, rollout_mode = choose_model_version()

        severity, confidence = predict_with_model(request.message, selected_model)

        if selected_model == "v1":
            metrics["model_v1_requests"] += 1
        else:
            metrics["model_v2_requests"] += 1

        shadow_prediction = None

        if rollout_config["shadow_enabled"] and selected_model == "v1":
            shadow_severity, shadow_confidence = predict_with_model(request.message, "v2")

            metrics["shadow_evaluations"] += 1

            if shadow_severity != severity:
                metrics["shadow_disagreements"] += 1

            shadow_prediction = {
                "model_version": "v2",
                "severity": shadow_severity,
                "confidence": shadow_confidence,
                "used_for_decision": False
            }

        latency_ms = round((perf_counter() - start) * 1000, 2)
        record_latency(latency_ms)

        return PredictionResponse(
            severity=severity,
            confidence=confidence,
            model_version=selected_model,
            rollout_mode=rollout_mode,
            latency_ms=latency_ms,
            shadow_prediction=shadow_prediction
        )

    except Exception:
        metrics["errors"] += 1
        raise


@app.get("/metrics")
def get_metrics():
    latencies = metrics["latencies_ms"]

    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0

    p95_latency = 0
    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = int(0.95 * (len(sorted_latencies) - 1))
        p95_latency = round(sorted_latencies[p95_index], 2)

    shadow_disagreement_rate = 0
    if metrics["shadow_evaluations"] > 0:
        shadow_disagreement_rate = round(
            metrics["shadow_disagreements"] / metrics["shadow_evaluations"],
            4
        )

    return {
        "total_requests": metrics["total_requests"],
        "errors": metrics["errors"],
        "model_v1_requests": metrics["model_v1_requests"],
        "model_v2_requests": metrics["model_v2_requests"],
        "shadow_evaluations": metrics["shadow_evaluations"],
        "shadow_disagreements": metrics["shadow_disagreements"],
        "shadow_disagreement_rate": shadow_disagreement_rate,
        "average_latency_ms": avg_latency,
        "p95_latency_ms": p95_latency,
        "latest_latencies_ms": latencies[-10:],
        "current_rollout_config": rollout_config
    }


@app.get("/rollout/config")
def get_rollout_config():
    return rollout_config


@app.post("/rollout/config")
def update_rollout_config(config: RolloutConfig):
    rollout_config["active_model"] = config.active_model
    rollout_config["shadow_enabled"] = config.shadow_enabled
    rollout_config["canary_percent"] = config.canary_percent

    return {
        "message": "Rollout configuration updated",
        "config": rollout_config
    }
