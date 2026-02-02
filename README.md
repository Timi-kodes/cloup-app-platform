# Project Intention

## I worked on this project to learn how **real production patterns** is used by devops teams. This project tasks was designed/generated with the help of ChatGPT to emulate real task in the companies/industry

# Cloud App Platform Project

A production-oriented, containerized backend deployed on AWS using Terraform, automated CI/CD, and built-in observability.  
My focuses were on **system design, reliability, and operational correctness**.

---

## What This Project Demonstrates

- Reproducible cloud infrastructure using Terraform
- Serverless container orchestration with ECS Fargate
- Secure CI/CD using GitHub Actions with OIDC (no static AWS keys)
- Load-balanced, health-checked deployments
- Centralized logging and operational metrics
- Self-healing behavior under failure

---

## High-Level Architecture

- VPC with public subnets
- ALB → ECS Fargate service
- ECR for images
- CloudWatch for logs/metrics
- GitHub Actions with OIDC for CI/CD

---

## Why These Design Choices

### ECS Fargate (No EC2)

- Removes server management overhead (patching, scaling, SSH)
- Focuses on orchestration, deployment safety, and reliability
- Matches how many modern teams run container workloads

### Terraform

- Infrastructure is declarative, versioned, and reproducible
- Remote state with locking prevents accidental corruption
- Clear separation of concerns (network, compute, CI/CD)

### GitHub Actions + OIDC

- No long-lived AWS access keys
- Identity-based, short-lived credentials
- Repository and branch-level trust boundaries

### Health Checks & Load Balancer

- Bad deployments are blocked automatically
- Traffic only reaches healthy tasks
- Failure is contained, not catastrophic

---

## Repository Structure

cloud-app-platform/
├── app/
│ ├── main.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── terraform/
│ ├── backend/
│ ├── network/
│ └── ecs/
│ ├── main.tf
│ ├── data.tf
│ ├── variables.tf
│ ├── terraform.tfvars
│ ├── github-oidc.tf
│ └── alarms.tf
│
├── .github/
│ └── workflows/
│ └── deploy.yml
│
├── .gitignore
└── README.md

---

## Application Endpoints

- `GET /health`  
  Used by the load balancer and ECS to determine task health.

- `GET /orders`  
  Example business endpoint for traffic and latency testing.

- `GET /metrics`  
  Prometheus-formatted application metrics.

---

## Deployment Flow

1. Code is pushed to the `main` branch
2. GitHub Actions builds the Docker image
3. Image is pushed to Amazon ECR
4. ECS service is redeployed automatically
5. Load balancer health checks gate traffic
6. Old tasks are replaced safely

There is **no manual deployment step**.

---

## Observability & Reliability

### Logs

- All container logs are sent to CloudWatch
- Each task has its own log stream
- Logs are available immediately on startup

### Metrics

- ECS provides CPU and memory metrics
- ALB provides request and error metrics
- Application exposes `/metrics` for future scraping

### Alarms

- CloudWatch alarms are defined as code
- Alerts are based on service-level signals, not guesswork

---

## Failure Handling (Intentional Testing)

This system was intentionally broken to verify behavior:

- Killing a running task causes ECS to replace it automatically
- Returning a failing `/health` response blocks traffic
- Bad deployments never receive production requests

This confirms the system **fails safely**.

---

## Configuration & Security Notes

- No AWS credentials are stored in the repository
- GitHub Actions uses OIDC with scoped IAM permissions
- `terraform.tfvars` contains only non-sensitive values
- Terraform state is remote and locked

---

## How to Destroy Everything

Clean teardown is part of operational discipline.

```bash
cd terraform/ecs && terraform destroy
cd ../network && terraform destroy
cd ../backend && terraform destroy
```
