# Cloud Cost Optimization System - Data Flow Diagram

```mermaid
flowchart TD
    A[Azure Subscription] --> B[Azure Resource Manager API]
    A --> C[Azure Monitor Metrics API]
    A --> D[Azure Cost Management API]

    B --> E[Resource Discovery Module]
    C --> F[Metric Collection Module]
    D --> G[Cost Collection Module]

    E --> H[Resource Inventory]
    F --> I[Normalized Resource Metrics]
    G --> J[Normalized Cost Records]

    H --> K[(SQLite Database)]
    I --> K
    J --> K

    K --> L[Optimization Engine]
    L --> M[Recommendations]
    L --> N[Savings Estimates]

    M --> O[CSV Export]
    N --> O
    I --> O
    J --> O

    O --> P[Power BI / Reporting Dashboard]
    K --> Q[FastAPI Backend]
    Q --> R[REST Endpoints]
    R --> S[User / Dashboard / API Clients]

    T[Service Principal / Azure Credentials] --> B
    T --> C
    T --> D
```

## Flow Description

1. Azure credentials authenticate the application using a service principal.
2. Azure Resource Manager lists all resources inside the subscription.
3. Azure Monitor Metrics API retrieves CPU, storage, and other performance data.
4. Azure Cost Management API retrieves cost information for the subscription.
5. The collector modules normalize the raw responses into structured rows.
6. Data is stored in SQLite tables such as resource_metrics, cost_records, recommendations, and savings_estimates.
7. The optimization engine reads the latest data and generates recommendations and estimated savings.
8. Export scripts generate CSV files used for reporting, dashboards, and further analysis.
9. The FastAPI backend exposes endpoints to access the processed data.

## Main Components

- Azure Subscription: source of resources, metrics, and billing data
- Resource Discovery: identifies Azure services and resources
- Metric Collection: gathers utilization data for compute/storage resources
- Cost Collection: fetches Azure billing data
- Persistence Layer: stores structured data in SQLite
- Optimization Engine: applies rules to detect inefficiencies and estimate savings
- Reporting Layer: exports CSV files for visualization and analytics
- API Layer: exposes the project data through FastAPI endpoints
```
