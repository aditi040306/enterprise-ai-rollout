import hashlib


def _confidence_from_text(text, base):
    hash_value = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
    variation = (hash_value % 20) / 100
    return round(min(base + variation, 0.99), 4)


def predict_v1(text):
    lower_text = text.lower()

    if any(word in lower_text for word in ["outage", "down", "critical", "unavailable", "payment failure"]):
        severity = "Critical"
        confidence = _confidence_from_text(text, 0.72)
    elif any(word in lower_text for word in ["timeout", "latency", "failed", "error", "exception"]):
        severity = "High"
        confidence = _confidence_from_text(text, 0.65)
    elif any(word in lower_text for word in ["warning", "slow", "retry", "degraded"]):
        severity = "Medium"
        confidence = _confidence_from_text(text, 0.58)
    else:
        severity = "Low"
        confidence = _confidence_from_text(text, 0.50)

    return {
        "severity": severity,
        "confidence": confidence,
        "model_version": "v1"
    }


def predict_v2(text):
    lower_text = text.lower()

    if any(word in lower_text for word in ["outage", "down", "critical", "unavailable", "payment failure", "database"]):
        severity = "Critical"
        confidence = _confidence_from_text(text, 0.76)
    elif any(word in lower_text for word in ["timeout", "latency", "failed", "error", "exception", "api"]):
        severity = "High"
        confidence = _confidence_from_text(text, 0.70)
    elif any(word in lower_text for word in ["warning", "slow", "retry", "degraded", "queue"]):
        severity = "Medium"
        confidence = _confidence_from_text(text, 0.62)
    else:
        severity = "Low"
        confidence = _confidence_from_text(text, 0.54)

    return {
        "severity": severity,
        "confidence": confidence,
        "model_version": "v2"
    }