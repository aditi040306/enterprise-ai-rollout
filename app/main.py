from fastapi import FastAPI, HTTPException
import time

from api.schemas import IncidentPredictionRequest, RolloutConfigUpdateRequest
from api.model_router import predict_with_rollout
from rollout.rollout_manager import rollout_manager
from monitoring.metrics import metrics_store
from queue_worker.worker import async_prediction_queue


app = FastAPI(
    title="Enterprise AI Rollout Testbed",
    description="AI API scaling prototype with shadow deployment, canary rollout, async processing, and monitoring.",
    version="3.0.0"
)


@app.on_event("startup")
def startup_event():
    async_prediction_queue.start(
        predict_function=predict_with_rollout,
        metrics_store=metrics_store
    )


@app.on_event("shutdown")
def shutdown_event():
    async_prediction_queue.stop()


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Rollout Testbed API",
        "week": 3,
        "features": [
            "synchronous prediction",
            "asynchronous prediction",
            "shadow deployment",
            "canary rollout",
            "monitoring metrics"
        ]
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict_sync(request: IncidentPredictionRequest):
    start_time = time.time()

    try:
        prediction = predict_with_rollout(request.incident_text)
        latency_ms = (time.time() - start_time) * 1000

        metrics_store.record_request(
            request_type="sync",
            model_version=prediction.get("model_version", "v1"),
            latency_ms=latency_ms,
            success=True
        )

        prediction["latency_ms"] = round(latency_ms, 4)

        return prediction

    except Exception as exception:
        latency_ms = (time.time() - start_time) * 1000

        metrics_store.record_request(
            request_type="sync",
            model_version="unknown",
            latency_ms=latency_ms,
            success=False
        )

        raise HTTPException(status_code=500, detail=str(exception))


@app.post("/predict/async")
def predict_async(request: IncidentPredictionRequest):
    return async_prediction_queue.submit_job(request.incident_text)


@app.get("/predict/async/{job_id}")
def get_async_prediction(job_id: str):
    job = async_prediction_queue.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@app.get("/queue/status")
def get_queue_status():
    return async_prediction_queue.status()


@app.get("/metrics")
def get_metrics():
    return metrics_store.snapshot(
        queue_size=async_prediction_queue.queue_size()
    )


@app.get("/rollout/config")
def get_rollout_config():
    return rollout_manager.get_config()


@app.post("/rollout/config")
def update_rollout_config(request: RolloutConfigUpdateRequest):
    if hasattr(request, "model_dump"):
        updates = request.model_dump(exclude_unset=True)
    else:
        updates = request.dict(exclude_unset=True)

    return rollout_manager.update_config(updates)