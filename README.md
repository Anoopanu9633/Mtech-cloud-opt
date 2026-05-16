# Cloud Cost Optimization System using Microsoft Azure

This project is an M.Tech-level cloud optimization platform built with Python, FastAPI, Azure SDKs, Docker, and GitHub Actions.

## Overview

The system collects Azure resource metrics and cost data, detects underutilized or idle resources, generates optimization recommendations, and estimates monthly savings.

### Key Features

- Azure resource discovery and cost collection
- VM and storage utilization metrics
- Rule-based optimization recommendations
- Savings estimation after applying recommendations
- REST APIs via FastAPI
- SQLite data persistence with easy PostgreSQL/Azure SQL migration
- Docker and GitHub Actions CI/CD
- Power BI dashboard data preparation
- Optional Kubernetes deployment manifests

## Architecture

The architecture is split into logical modules:

- `backend/` - FastAPI application and REST endpoints
- `collector/` - Azure data integration and metric collection
- `optimizer/` - Recommendation and savings engine
- `database/` - SQLAlchemy models and persistence layer
- `dashboard/` - Power BI dataset preparation and reporting guidance
- `docker/` - compose files and Docker configuration
- `k8s/` - Kubernetes deployment manifests

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker
- Azure CLI or service principal credentials
- GitHub account for GitHub Actions integration

### Azure Prerequisites

1. Create or reuse an Azure subscription.
2. Enable Cost Management API access.
3. Create a service principal with `Contributor` or `Reader` access.
4. Assign `Cost Management Reader` and `Monitoring Reader` to the service principal.

### Environment Variables

Set these values in your environment or in a `.env` file:

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP` (optional for scoped queries)

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run Locally

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t cloud-cost-optimizer .
docker run --rm -p 8000:8000 --env-file .env cloud-cost-optimizer
```

### GitHub Actions

The workflow in `.github/workflows/ci-cd.yml` runs tests, builds the image, and validates the deployment steps.

## Folder Structure

- `backend/` - API application
- `collector/` - Azure data connectors
- `optimizer/` - cost and utilization rules
- `database/` - SQLite models and repository
- `dashboard/` - Power BI dataset and visualization guidance
- `docker/` - Docker Compose and helpers
- `k8s/` - Kubernetes manifests
- `.github/workflows/` - CI/CD pipeline

## Notes

This repository is designed as a production-style project structure suitable for academic research and portfolio presentation.
