# Implementation & Build Process

## Overview

This document describes the step-by-step process to create and run the Cloud Cost Optimization System using Microsoft Azure. It covers the technologies used, required tools, project structure, development phases, and the architecture diagram.

## Requirements

### Software Requirements

- Python 3.11 or 3.14
- Git
- Docker
- Azure CLI (optional, for authentication)
- A code editor such as Visual Studio Code
- GitHub account for repository and GitHub Actions

### Azure Requirements

- Azure subscription
- Service principal with the following permissions:
  - `Cost Management Reader`
  - `Monitoring Reader`
  - `Reader` or higher on the target resource scope
- Azure resource group and at least one active resource (VM, storage, etc.)

### Project Dependencies

Install the dependencies from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or export the following environment variables:

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_SUBSCRIPTION_ID`
- `DATABASE_URL` (optional, default is `sqlite:///./cloud_cost_optimizer.db`)

## Languages and Tools Used

- **Python**: core application logic, Azure SDK integration, data processing
- **FastAPI**: backend REST API framework
- **SQLAlchemy**: database modeling and persistence layer
- **Docker**: containerization
- **GitHub Actions**: CI/CD automation
- **Power BI**: visualization and reporting
- **YAML**: workflow and Kubernetes manifest configuration
- **Markdown**: documentation and report files

## Step-by-Step Creation Process

### Step 1: Setup Project Structure

Create the following folders:

- `backend/`
- `collector/`
- `optimizer/`
- `database/`
- `dashboard/`
- `docker/`
- `k8s/`
- `.github/workflows/`
- `docs/`

Add initial files:

- `backend/main.py`
- `collector/azure_client.py`
- `collector/data_fetcher.py`
- `optimizer/engine.py`
- `database/db.py`
- `database/models.py`
- `database/repository.py`
- `docker/Dockerfile`
- `.github/workflows/ci-cd.yml`

### Step 2: Configure the Database

Use SQLAlchemy to define models for:

- `ResourceMetric`
- `CostRecord`
- `Recommendation`
- `SavingsEstimate`

Implement a DB initialization function in `database/db.py`.

### Step 3: Build Azure Integration

Implement Azure clients in `collector/azure_client.py`:

- `DefaultAzureCredential` authentication
- `ResourceManagementClient` for resource discovery
- `MetricsQueryClient` for performance metrics
- `CostManagementClient` for cost data

Create data-fetching logic in `collector/data_fetcher.py` to:

- discover resources
- query metrics
- query cost data
- save results to the database

### Step 4: Create Backend APIs

Build `backend/main.py` with endpoints for:

- `/get-costs`
- `/get-resource-utilization`
- `/get-recommendations`
- `/get-savings`
- `/get-idle-resources`

Set up FastAPI with dependency injection for DB sessions.

### Step 5: Implement the Optimization Engine

Create `optimizer/engine.py` with rule-based recommendations:

- CPU underutilized rule
- unattached disk rule
- non-production shutdown rule

Store generated recommendations and savings estimates in the database.

### Step 6: Add Dashboard Export Support

Implement Power BI export support in `dashboard/powerbi/data_prep.py`.

This prepares CSV files containing:

- cost records
- utilization metrics
- recommendations and estimated savings

### Step 7: Containerize the Application

Create `Dockerfile` and `docker/docker-compose.yml`.

The Dockerfile should:

- install Python dependencies
- copy project files
- run `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

### Step 8: Add CI/CD Workflow

Configure `.github/workflows/ci-cd.yml` to:

- checkout source
- install dependencies
- run tests
- build Docker image

### Step 9: Optional Kubernetes Deployment

Add `k8s/deployment.yaml` and `k8s/service.yaml` for future scaling in AKS or any Kubernetes cluster.

## How the Process Works

### User / Developer Workflow

1. Developer clones the repository.
2. They install dependencies and configure Azure credentials.
3. The FastAPI app is started locally.
4. A user calls API endpoints to collect data and fetch results.

### Internal Application Workflow

1. **API receives request**
   - FastAPI endpoint is called.
2. **Collector fetches Azure data**
   - Resource discovery
   - Metrics query
   - Cost query
3. **Database saves records**
   - Metrics and cost rows are persisted
4. **Optimizer evaluates data**
   - Categories idle or underutilized resources
   - Generates recommendations
5. **Results are returned**
   - API returns JSON responses
6. **Dashboard export**
   - CSV is generated for Power BI reporting

## Architecture Diagram

```text
         +-----------------------+
         |   Azure Resources     |
         | (VMs, Disks, Storage) |
         +----------+------------+
                    |
                    v
    +---------------+-----------------+
    | Azure Monitor + Cost Management |
    |    API Layer (Telemetry & Cost) |
    +---------------+-----------------+
                    |
                    v
           +--------+---------+
           | Data Collection  |
           |   Layer          |
           | (collector/*)    |
           +--------+---------+
                    |
                    v
           +--------+---------+
           | Optimization      |
           | Engine            |
           | (optimizer/*)     |
           +--------+---------+
                    |
                    v
    +---------------+-----------------+
    |   Database Layer               |
    | (SQLite / Azure SQL / Postgres)|
    +---------------+-----------------+
                    |
                    v
           +--------+---------+
           | API / Reporting   |
           | (FastAPI + PowerBI)|
           +-------------------+
```

## Commands to Run the Application

```bash
cd "c:\Users\preet\Downloads\Cloud Optimization"
python -m pip install -r requirements.txt
copy .env.example .env
# populate .env with Azure values
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Then use the endpoints:

```bash
curl http://localhost:8000/get-costs
curl http://localhost:8000/get-resource-utilization
curl http://localhost:8000/get-recommendations
curl http://localhost:8000/get-savings
curl http://localhost:8000/get-idle-resources
```

## Summary

This application is built using Python and FastAPI for the backend, Azure SDKs for cloud integration, SQLAlchemy for database persistence, Docker for containerization, and GitHub Actions for CI/CD. The system collects Azure cost and usage data, applies optimization rules, stores results, and exports dashboard-ready reports for Power BI.
