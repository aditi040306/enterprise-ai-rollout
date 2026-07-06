# Project Scope and 3-Month Roadmap

## Enterprise AI Rollout Project

This project has enough scope to be developed over approximately three months. The work will be completed in phases, starting with research analysis and a minimal prototype, and gradually expanding into a full AI scaling and API integration testbed.

The project will not be limited to building only an AI model. Instead, it will focus on the complete journey of converting an AI model into an enterprise-ready AI service. This includes API-based integration, monitoring, scaling, model versioning, safe rollout, and rollback mechanisms.

## Month 1: Research Foundation and Initial Prototype

The first month will focus on understanding the problem, defining the architecture, and building the first working version of the prototype.

During this phase, I will:

* Review class materials related to AI Scaling, AI-as-a-Service, enterprise API integration, MLOps, monitoring, and continuous improvement.
* Define the research question and project scope.
* Prepare project explanation and milestone documents.
* Select software incident severity prediction as the initial AI use case.
* Create a small sample incident dataset.
* Build a simple baseline AI model for severity classification.
* Expose the model through a basic API.
* Add health check, prediction, feedback, and metrics endpoints.
* Push the initial documentation and prototype structure to GitHub.

The expected output for Month 1 is a clear project foundation with initial documentation, architecture, baseline model, and working API prototype.

## Month 2: AI API Integration and Scaling Features

The second month will focus on expanding the prototype into a more enterprise-style AI service.

During this phase, I will:

* Improve the API structure and model routing logic.
* Add model versioning using model v1 and model v2.
* Implement synchronous REST API prediction.
* Add asynchronous queue-based processing for high-volume requests.
* Add basic monitoring for latency, throughput, request count, and error rate.
* Add shadow deployment logic where model v2 can run silently while model v1 remains active.
* Add canary rollout logic where a small percentage of traffic can be routed to model v2.
* Start comparing synchronous and asynchronous prediction patterns.

The expected output for Month 2 is a stronger AI API service that supports model versioning, async processing, monitoring, shadow deployment, and canary rollout.

## Month 3: Experiments, Dashboard, and Final Research Output

The third month will focus on running experiments, analyzing results, and preparing the final project output.

During this phase, I will:

* Run load testing to compare latency and throughput under different traffic levels.
* Compare synchronous API calls with asynchronous queue-based processing.
* Analyze model v1 and model v2 behavior under shadow and canary deployment.
* Add rollback logic based on latency, error rate, or poor model behavior.
* Build a simple dashboard to show metrics such as latency, throughput, request count, model version usage, and rollout status.
* Document experiment results in tables and charts.
* Prepare final GitHub README, architecture diagram, and research summary.
* Write limitations and future improvement sections.

The expected output for Month 3 is a complete AI scaling and API integration testbed with documentation, working prototype, monitoring dashboard, experiment results, and final research explanation.

## Final Project Outcome

By the end of the three months, the project should demonstrate how an AI model can be moved from a simple prototype into an enterprise-style AI service. The final project will show how the model is exposed through APIs, monitored, scaled, versioned, tested under traffic, and safely rolled out using shadow deployment, canary release, and rollback mechanisms.

Overall, the three-month scope is appropriate because the project includes both research and implementation. It begins with analysis and documentation, then moves into prototype development, and finally expands into experiments, evaluation, and reporting.
