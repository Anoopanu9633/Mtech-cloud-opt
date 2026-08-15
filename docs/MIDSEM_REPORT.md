# MIDSEM REPORT: Resource Lifecycle Analytics Platform (RLAP)

## 1. MODULES

### 1.1 Backend API Module
- Implements the REST API using **FastAPI**.
- Provides endpoints for health checks, cost retrieval, resource utilization, optimization recommendations, savings estimates, and idle resource detection.
- Handles request routing, dependency injection, and response serialization.
- Loads configuration from environment variables using `.env`.

### 1.2 Azure Data Collector Module
- Interfaces with **Azure SDKs** to collect telemetry from Azure Monitor and cost data from Azure Cost Management.
- Discovers Azure resources in the configured subscription.
- Queries metrics such as CPU utilization, disk I/O, and storage usage.
- Fetches cost records and associates them with subscription and service information.
- Manages Azure authentication using a service principal.

### 1.3 Optimization Engine Module
- Applies rule-based logic to identify underutilized resources.
- Detects conditions such as low CPU utilization, unused disks, idle storage, and inefficient VM sizing.
- Generates optimization recommendations for shutdown, resizing, archiving, and cost reduction.
- Computes estimated monthly savings for each recommendation.

### 1.4 Database Persistence Module
- Implements local persistence using **SQLAlchemy** and **SQLite**.
- Defines ORM models for resource metrics, cost records, recommendations, and savings estimates.
- Provides repository methods for saving and retrieving collected data.
- Supports future migration to **PostgreSQL** or **Azure SQL Database**.

### 1.5 Reporting and Dashboard Module
- Prepares exported data for visualization in **Power BI**.
- Generates CSV reports for cost, utilization, recommendations, and savings.
- Provides sample data files that can be loaded into dashboards.
- Supports visualization of trends, heatmaps, and recommendation summaries.

### 1.6 Infrastructure and Deployment Module
- Contains Docker and Docker Compose configuration for containerized deployment.
- Includes Kubernetes manifests for optional scalable deployment.
- Supports CI/CD automation with GitHub Actions.

## 2. FUNCTIONAL BLOCK DIAGRAM / DESCRIPTION

### Functional Block Diagram
```text
[User / Scheduler]
      ↓
[FastAPI REST API] ────────────────┐
      ↓                          │
[Azure Data Collector]            │
      ↓                          │
[Azure Monitor & Cost APIs]      │
      ↓                          │
[Database Persistence] <─────────┘
      ↓
[Optimization Engine]
      ↓
[Recommendations + Savings]
      ↓
[Power BI / Dashboard Export]
```

### Description
1. **User / Scheduler**: Initiates API calls manually or via an automated scheduler.
2. **FastAPI REST API**: Serves endpoints for health, data retrieval, and recommendations.
3. **Azure Data Collector**: Fetches live resource inventory, metrics, and cost data from Azure.
4. **Azure Monitor & Cost APIs**: Azure platform services that provide telemetry and cost analytics.
5. **Database Persistence**: Stores collected metrics, cost records, recommendations, and savings estimates.
6. **Optimization Engine**: Analyzes persisted data to detect inefficiencies and create actionable recommendations.
7. **Recommendations + Savings**: Returns optimization insight and potential cost savings to users.
8. **Power BI / Dashboard Export**: Generates CSV exports for visualization and reporting.

## 3. MAJOR TECHNICAL SPECIFICATIONS OF RLAP

### 3.1 Platform and Language
- **Primary Language**: Python 3.14
- **Web Framework**: FastAPI
- **Cloud Provider**: Microsoft Azure

### 3.2 Azure Integration
- **Authentication**: Azure Service Principal
- **Azure SDKs**:
  - `azure-identity`
  - `azure-mgmt-costmanagement`
  - `azure-mgmt-resource`
  - `azure-monitor-query`
- **Role Requirements**:
  - Cost Management Reader
  - Monitoring Reader
  - Reader on subscription

### 3.3 Data Storage
- **ORM**: SQLAlchemy
- **Database**: SQLite for local development
- **Schema**:
  - `resource_metrics`
  - `cost_records`
  - `recommendations`
  - `savings_estimates`

### 3.4 Deployment
- **Containerization**: Docker
- **Orchestration**: Kubernetes manifests provided (optional)
- **CI/CD**: GitHub Actions workflow for testing and build automation

### 3.5 Reporting and Visualization
- **Export Format**: CSV
- **Target Visualization Tool**: Power BI
- **Report Types**:
  - Cost trends
  - Resource utilization
  - Idle resource summary
  - Suggestion and savings dashboard

### 3.6 APIs and Endpoints
- `/health` — Service health status
- `/get-costs` — Cost data retrieval
- `/get-resource-utilization` — Resource utilization metrics
- `/get-recommendations` — Optimization suggestions
- `/get-savings` — Savings estimates
- `/get-idle-resources` — Idle resource discovery

## 4. DESIGN CONSIDERATIONS

### 4.1 Modularity
- Separate modules for API, data collection, optimization, persistence, and reporting.
- Easier maintenance and future extension.

### 4.2 Scalability
- Docker and Kubernetes support enable deployment to scaled environments.
- Database layer abstracted to support migration to more robust SQL engines.

### 4.3 Security
- Sensitive information is stored in environment variables (`.env`) and ignored by Git.
- Azure service principal handles secure API authentication.
- Minimal permissions principle: service principal uses read-only cost and monitoring roles.

### 4.4 Fault Tolerance
- Collector catches Azure SDK exceptions and degrades gracefully.
- Empty or partial data is handled without crashing the API.

### 4.5 Extensibility
- New Azure metrics, cost rules, or optimization heuristics can be added without changing the API layer.
- Reporting module can be extended to support additional BI tools.

### 4.6 Maintainability
- Uses common Python patterns and dependency management.
- Clear folder structure separates concerns.
- Documentation and testing enable easier knowledge transfer.

## 5. FUTURE PLAN

### 5.1 Dashboard and Visualization
- Build a full Power BI dashboard for cost trends, utilization heatmaps, and savings analytics.
- Add interactive report pages for idle resources and recommendation follow-up.

### 5.2 CI/CD and Azure Deployment
- Deploy containerized application to Azure Container Registry (ACR).
- Use Azure Kubernetes Service (AKS) or Azure App Service for production deployment.
- Configure GitHub Actions to publish Docker images and deploy automatically.

### 5.3 Scheduling and Automation
- Implement a scheduled collector using APScheduler, Celery, or cron jobs.
- Automate daily or hourly data refresh and recommendation updates.

### 5.4 Secrets Management
- Migrate sensitive configuration to **Azure Key Vault**.
- Use GitHub Secrets for CI/CD pipeline variables.

### 5.5 Frontend Dashboard/UI
- Add a lightweight frontend dashboard for interactive display of recommendations and cost savings.
- Use React, Vue, or a similar frontend framework for user experience.

### 5.6 Advanced Optimization
- Add machine-learning-based anomaly detection and trend forecasting.
- Introduce dynamic right-sizing recommendations based on historic usage.
- Support multi-subscription analysis and cross-resource optimization.
