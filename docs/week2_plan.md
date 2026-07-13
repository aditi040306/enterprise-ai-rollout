# Week 2 Plan  
## Model Versioning, Shadow Deployment, and Canary Rollout

## Week 2 Objective

The goal for Week 2 is to extend the Week 1 AI API prototype by adding model versioning and safe rollout mechanisms. In Week 1, the project established the basic AI-as-a-Service flow where an incident message is sent to an API and the AI model returns a severity prediction.

In Week 2, the focus is on how enterprises can safely introduce a new AI model version without immediately replacing the existing model. This is important because production AI systems require monitoring, comparison, and rollback readiness before fully shifting traffic to a new model.

## Features Planned for Week 2

- Train and save two model versions: model v1 and model v2
- Add model routing logic in the API
- Add rollout configuration endpoint
- Add shadow deployment support
- Add canary rollout support
- Add metrics for model version usage
- Track shadow model comparisons
- Track latency and request counts

## Why This Matters

In an enterprise environment, a new AI model should not directly replace the old model. The new model must first be tested safely. Shadow deployment allows model v2 to run silently while model v1 still serves the real response. Canary rollout allows a small percentage of traffic to be routed to model v2 before a full release.

This Week 2 work connects directly to AI Scaling, AI-as-a-Service, MLOps, monitoring, and continuous improvement.
