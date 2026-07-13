# Week 2 Progress Report

For Week 2, I extended the initial AI API prototype by adding model versioning and safe rollout functionality. In Week 1, the system only supported a basic AI-as-a-Service flow where an incident message was sent to the API and the model returned a severity prediction. In Week 2, I added support for two model versions, v1 and v2, so the system can begin simulating how enterprises safely test and roll out new AI models.

I updated the training script to generate separate model artifacts for model v1 and model v2. I also updated the FastAPI service to include model routing, confidence score, rollout mode, and shadow prediction support. The API response now shows not only the predicted severity, but also the model version used, the confidence score, the rollout mode, latency, and optional shadow model output.

The main Week 2 feature implemented is shadow deployment. In this setup, model v1 continues to serve the actual API response, while model v2 runs silently in the background. Model v2 produces a shadow prediction, but it is not used for the real decision. This allows a new model version to be evaluated safely before sending real traffic to it.

I tested the shadow deployment flow successfully. The API returned a response where model v1 handled the actual prediction and model v2 returned a separate shadow prediction with `used_for_decision` set to false. This confirms that the system can compare a new AI model version without affecting the user-facing result.

This Week 2 work moves the project from a basic AI API prototype toward an enterprise AI rollout system. The project now demonstrates model versioning, rollout configuration, shadow deployment, confidence scoring, and expanded monitoring fields. These features create the foundation for adding canary rollout, A/B testing, rollback logic, and more detailed scaling experiments in the next phase.
