from threading import Lock
from statistics import mean


class MetricsStore:
    def __init__(self):
        self._lock = Lock()
        self.total_requests = 0
        self.sync_requests = 0
        self.async_requests = 0
        self.failed_requests = 0
        self.model_v1_requests = 0
        self.model_v2_requests = 0
        self.latencies_ms = []

    def record_request(self, request_type, model_version, latency_ms, success=True):
        with self._lock:
            self.total_requests += 1

            if request_type == "async":
                self.async_requests += 1
            else:
                self.sync_requests += 1

            if model_version == "v2":
                self.model_v2_requests += 1
            else:
                self.model_v1_requests += 1

            if not success:
                self.failed_requests += 1

            self.latencies_ms.append(round(latency_ms, 4))

    def snapshot(self, queue_size=0):
        with self._lock:
            average_latency = round(mean(self.latencies_ms), 4) if self.latencies_ms else 0

            sorted_latencies = sorted(self.latencies_ms)
            if sorted_latencies:
                p95_index = int(0.95 * (len(sorted_latencies) - 1))
                p95_latency = round(sorted_latencies[p95_index], 4)
            else:
                p95_latency = 0

            return {
                "total_requests": self.total_requests,
                "sync_requests": self.sync_requests,
                "async_requests": self.async_requests,
                "failed_requests": self.failed_requests,
                "model_v1_requests": self.model_v1_requests,
                "model_v2_requests": self.model_v2_requests,
                "average_latency_ms": average_latency,
                "p95_latency_ms": p95_latency,
                "queue_size": queue_size
            }


metrics_store = MetricsStore()