
## What am I trying to do?

We are building a **mini enterprise AI system**.

Not just a model.
Not just an API.
The project is about:

**How an AI model is exposed through APIs and scaled safely in an enterprise system.**

---

## Where is the AI?

The AI is the part that reads an incident/log message and predicts the severity.

Example:

```text
Input:
"Payment API is timing out and downstream billing service is unavailable."

AI prediction:
Critical
```

Another example:

```text
Input:
"Minor typo found on the settings page."

AI prediction:
Low
```

So the AI model is doing **text classification**.

It takes unstructured text and classifies it into:

```text
Low
Medium
High
Critical
```

This is the AI part.

Right now, Week 1 uses a simple ML model:

```text
TF-IDF + Logistic Regression
```

Later, we can make it more AI-heavy by adding:

```text
LLM-based severity prediction
RAG-based incident context retrieval
explanation generation
confidence scoring
feedback-based improvement
```

---

## Then where does API integration come in?

The AI model should not stay inside a notebook.

In real enterprise systems, another application should be able to call the model through an API.

So we expose the AI model like this:

```text
Enterprise App / Monitoring Tool
        ↓
POST /predict-severity
        ↓
AI Model
        ↓
Severity Prediction
```

Example API call:

```json
{
  "message": "Kafka consumer lag is increasing and order events are delayed"
}
```

API response:

```json
{
  "severity": "High",
  "model_version": "v1",
  "latency_ms": 5.2
}
```

That is **AI-as-a-Service**.

The model becomes a service that other enterprise systems can use.

---

## Where does AI Scaling come in?

Once the AI model is available through an API, the next question is:

**Can this AI service work reliably when many users or systems call it?**

That is the scaling part.

We will test:

```text
Can the API respond quickly?
Can it handle more requests?
What happens when traffic increases?
Should prediction be synchronous or asynchronous?
How do we monitor latency and throughput?
How do we release a new model safely?
How do we roll back if the new model is bad?
```

So the project is not just asking:

**“Can the model predict severity?”**

It is asking:

**“Can this AI model be deployed, integrated, monitored, scaled, versioned, and safely rolled out like a real enterprise AI service?”**

That is the actual project idea.

---

## How this relates to our project idea

Your project idea was:

**AI Scaling + AI-API Integration**

This project directly matches that:

### 1. AI

Incident severity prediction model.

### 2. API Integration

Expose the model through FastAPI endpoints.

```text
POST /predict-severity
GET /metrics
POST /feedback
POST /rollout/config
```

### 3. Scaling

Compare different ways of serving the AI model:

```text
Synchronous REST API
Asynchronous queue-based processing
Batch/high-volume processing
```

### 4. Safe Production Rollout

Test enterprise rollout methods:

```text
Shadow deployment
Canary release
A/B testing
Rollback
```

### 5. Monitoring

Track production-style metrics:

```text
Latency
Throughput
Error rate
p95 response time
Model version usage
Failed requests
```

---

## Simple analogy

Think of the AI model like an engine.

But the research is not only about building the engine.

The research is about building the full vehicle around it:

```text
AI model = engine
API = way other systems use the engine
Monitoring = dashboard
Scaling = handling more speed/load
Canary/rollback = safety system
```

So the project is about **turning an AI model into an enterprise-ready AI service**.

---

## One-line explanation

**I am building a research prototype that takes a small AI model for incident severity prediction and studies how it can be exposed through APIs, scaled under traffic, monitored, versioned, and safely rolled out in an enterprise environment.**

That is the connection between AI, API integration, and AI scaling.


## Week 3: Scaling AI APIs with Async Processing and Canary Rollout

In Week 3, I extended the AI API prototype from model versioning and shadow deployment into a more scalable enterprise-style service. The focus was on asynchronous prediction processing, canary rollout, and operational monitoring.

### Objective

The goal of Week 3 was to evaluate how enterprise AI services can handle higher request volume while safely routing a small percentage of production traffic to a newer model version.

### Features Added

- Synchronous prediction endpoint
- Asynchronous prediction endpoint
- Async job status retrieval
- Queue status endpoint
- Canary rollout configuration
- Model v1/v2 routing
- Shadow prediction support
- Monitoring metrics endpoint
- Basic load test script

### API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/predict` | POST | Runs synchronous prediction |
| `/predict/async` | POST | Submits prediction request to async queue |
| `/predict/async/{job_id}` | GET | Gets async job status and prediction result |
| `/queue/status` | GET | Returns queue size and worker status |
| `/metrics` | GET | Returns operational metrics |
| `/rollout/config` | GET | Returns rollout configuration |
| `/rollout/config` | POST | Updates rollout configuration |

### Canary Rollout

The Week 3 rollout configuration allows a controlled percentage of traffic to be routed to model v2 while model v1 remains the active model.

Example configuration:

```json
{
  "active_model": "v1",
  "shadow_enabled": true,
  "canary_enabled": true,
  "canary_model": "v2",
  "canary_percent": 10
}

This means most requests continue using model v1, while a small percentage of requests are routed to model v2.

Load Test Result

A basic load test was executed with 50 synchronous requests and 50 asynchronous requests.

Summary:

Total requests: 100
Sync requests: 50
Async requests: 50
Failed requests: 0
Model v1 requests: 92
Model v2 requests: 8
Queue size after processing: 0

The result shows that the API successfully handled both synchronous and asynchronous prediction requests while routing a portion of traffic to model v2 through canary rollout.