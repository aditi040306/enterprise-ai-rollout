from queue import Queue
from threading import Thread, Lock
from uuid import uuid4
from datetime import datetime
import time


class AsyncPredictionQueue:
    def __init__(self):
        self._queue = Queue()
        self._jobs = {}
        self._lock = Lock()
        self._running = False
        self._worker_thread = None
        self._predict_function = None
        self._metrics_store = None

    def start(self, predict_function, metrics_store):
        self._predict_function = predict_function
        self._metrics_store = metrics_store

        if self._running:
            return

        self._running = True
        self._worker_thread = Thread(target=self._run_worker, daemon=True)
        self._worker_thread.start()

    def stop(self):
        self._running = False

    def submit_job(self, incident_text):
        job_id = str(uuid4())

        job = {
            "job_id": job_id,
            "status": "queued",
            "incident_text": incident_text,
            "prediction": None,
            "error": None,
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None
        }

        with self._lock:
            self._jobs[job_id] = job

        self._queue.put(job_id)

        return {
            "job_id": job_id,
            "status": "queued",
            "message": "Prediction request accepted for async processing"
        }

    def get_job(self, job_id):
        with self._lock:
            return self._jobs.get(job_id)

    def queue_size(self):
        return self._queue.qsize()

    def status(self):
        return {
            "queue_size": self._queue.qsize(),
            "worker_running": self._running
        }

    def _run_worker(self):
        while self._running:
            if self._queue.empty():
                time.sleep(0.1)
                continue

            job_id = self._queue.get()

            with self._lock:
                job = self._jobs.get(job_id)
                if not job:
                    continue
                job["status"] = "processing"

            start_time = time.time()

            try:
                prediction = self._predict_function(job["incident_text"])
                latency_ms = (time.time() - start_time) * 1000

                with self._lock:
                    job["status"] = "completed"
                    job["prediction"] = prediction
                    job["completed_at"] = datetime.utcnow().isoformat()

                self._metrics_store.record_request(
                    request_type="async",
                    model_version=prediction.get("model_version", "v1"),
                    latency_ms=latency_ms,
                    success=True
                )

            except Exception as exception:
                latency_ms = (time.time() - start_time) * 1000

                with self._lock:
                    job["status"] = "failed"
                    job["error"] = str(exception)
                    job["completed_at"] = datetime.utcnow().isoformat()

                self._metrics_store.record_request(
                    request_type="async",
                    model_version="unknown",
                    latency_ms=latency_ms,
                    success=False
                )

            finally:
                self._queue.task_done()


async_prediction_queue = AsyncPredictionQueue()