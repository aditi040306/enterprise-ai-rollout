import requests
import time
from statistics import mean


BASE_URL = "http://127.0.0.1:8000"


SAMPLE_INCIDENTS = [
    "Payment API timeout increased and downstream database is unavailable.",
    "User login service is slow and retry count is increasing.",
    "Minor warning observed in background batch process.",
    "Application is down and customers cannot complete checkout.",
    "Queue processing is degraded but service is still available."
]


def configure_canary():
    response = requests.post(
        f"{BASE_URL}/rollout/config",
        json={
            "active_model": "v1",
            "shadow_enabled": True,
            "canary_enabled": True,
            "canary_model": "v2",
            "canary_percent": 10
        },
        timeout=10
    )

    print("Rollout Config:")
    print(response.json())


def send_sync_requests(total_requests=50):
    latencies = []

    for index in range(total_requests):
        incident_text = SAMPLE_INCIDENTS[index % len(SAMPLE_INCIDENTS)]

        start_time = time.time()

        response = requests.post(
            f"{BASE_URL}/predict",
            json={"incident_text": incident_text},
            timeout=10
        )

        latency_ms = (time.time() - start_time) * 1000
        latencies.append(latency_ms)

        body = response.json()

        print(
            f"SYNC {index + 1}: "
            f"status={response.status_code}, "
            f"model={body.get('model_version')}, "
            f"mode={body.get('rollout_mode')}, "
            f"latency_ms={round(latency_ms, 2)}"
        )

    print("\nSync Summary")
    print(f"Total sync requests: {total_requests}")
    print(f"Average sync latency ms: {round(mean(latencies), 2)}")


def send_async_requests(total_requests=50):
    job_ids = []
    acceptance_latencies = []

    for index in range(total_requests):
        incident_text = SAMPLE_INCIDENTS[index % len(SAMPLE_INCIDENTS)]

        start_time = time.time()

        response = requests.post(
            f"{BASE_URL}/predict/async",
            json={"incident_text": incident_text},
            timeout=10
        )

        latency_ms = (time.time() - start_time) * 1000
        acceptance_latencies.append(latency_ms)

        if response.status_code == 200:
            job_ids.append(response.json()["job_id"])

        print(
            f"ASYNC {index + 1}: "
            f"status={response.status_code}, "
            f"acceptance_latency_ms={round(latency_ms, 2)}"
        )

    print("\nAsync Summary")
    print(f"Total async jobs submitted: {len(job_ids)}")
    print(f"Average async acceptance latency ms: {round(mean(acceptance_latencies), 2)}")

    return job_ids


def print_metrics():
    response = requests.get(f"{BASE_URL}/metrics", timeout=10)

    print("\nMetrics:")
    print(response.json())


if __name__ == "__main__":
    configure_canary()

    print("\nRunning sync load test...")
    send_sync_requests(total_requests=50)

    print("\nRunning async load test...")
    send_async_requests(total_requests=50)

    time.sleep(2)

    print_metrics()