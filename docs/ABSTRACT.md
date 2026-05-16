Title: Cloud Cost Optimization System using Microsoft Azure

Abstract

Cloud service expenses represent a significant portion of IT budgets for enterprises and research institutions. This project, "Cloud Cost Optimization System using Microsoft Azure", presents a modular platform that collects Azure resource usage and cost data, identifies underutilized or idle resources, and provides actionable recommendations along with estimated monthly savings. The system is designed for practical deployment and academic evaluation, integrating Azure SDKs, telemetry from Azure Monitor, Cost Management APIs, and a rule-based optimization engine.

Methodology

The system architecture consists of a data collector, a persistence layer, an optimization engine, and RESTful APIs:

- Data Collector: Uses `azure-mgmt-resource`, `azure-monitor-query`, and `azure-mgmt-costmanagement` via `DefaultAzureCredential` to discover resources, query utilization metrics (CPU, disk I/O, storage usage), and fetch cost data. The collector normalizes data and persists it to a SQL database (SQLite by default with a path forward to PostgreSQL/Azure SQL).

- Persistence Layer: SQLAlchemy models store `ResourceMetric`, `CostRecord`, `Recommendation`, and `SavingsEstimate`. A repository layer provides read/write helpers to keep business logic separate from DB concerns.

- Optimization Engine: Implements rule-based detection for common waste patterns (e.g., sustained CPU < 10% suggests downsizing or shutdown; unattached disks flagged for deletion; non-production VMs scheduled for shutdown outside office hours). The engine estimates monthly savings conservatively by applying heuristics to historical cost and utilization data.

- APIs & Dashboard: A FastAPI backend exposes endpoints for fetching costs, utilization, recommendations, idle resources, and savings estimates. Processed data is prepared for Power BI in CSV format for visualization and reporting.

Implementation & Tools

- Language: Python
- Backend: FastAPI
- Database: SQLite (development), easily switched to PostgreSQL/Azure SQL via `DATABASE_URL`
- Azure SDKs: `azure-identity`, `azure-mgmt-resource`, `azure-monitor-query`, `azure-mgmt-costmanagement`
- Containerization: Docker + docker-compose; optional Kubernetes manifests for AKS
- CI/CD: GitHub Actions for tests and image building
- Visualization: Power BI (CSV data export provided)

Expected Results and Evaluation

The platform provides measurable outcomes: detection of idle resources, explicit recommendations to reduce cost, and estimated monthly savings. For evaluation, the system can be run against a subscription to collect 30 days of data and compare "before" and "after" monthly cost projections. Results will be validated by comparing actual cost reductions after applying recommendations (or via simulation of recommended actions).

Contributions

- A reusable, modular codebase for Azure cost monitoring and rule-based optimization.
- Integration guide and CI/CD pipeline for reproducible deployments.
- A Power BI data preparation pipeline to visualize cost and optimization impact.

Future Work

- Implement automated remediation (scheduled shutdowns, resizing, or deletion) with safe approval workflows.
- Replace rule-based heuristics with machine learning models to detect anomalous usage and suggest rightsizing driven by historical patterns.
- Integrate secrets management (Azure Key Vault) and managed identities for production-ready security.
- Add support for multi-cloud (AWS/GCP) cost aggregation and unified recommendations.

Keywords: Cloud cost optimization, Azure Cost Management, Azure Monitor, FastAPI, SQLAlchemy, Docker, Power BI
