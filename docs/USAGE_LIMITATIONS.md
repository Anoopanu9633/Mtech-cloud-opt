# Usage, Limitations, and Recommended Scenarios

## Purpose
This document describes how to use the Cloud Cost Optimization System (CCOS), where it is most applicable, its known limitations, and recommended production considerations.

## Quick Start (How to get data locally)
1. Copy `.env.example` to `.env` and populate Azure credentials (or set environment variables):

```powershell
$env:AZURE_TENANT_ID="your-tenant-id"
$env:AZURE_CLIENT_ID="your-client-id"
$env:AZURE_CLIENT_SECRET="your-client-secret"
$env:AZURE_SUBSCRIPTION_ID="your-subscription-id"
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Initialize DB (first run will create SQLite file automatically) and start the API:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. Trigger data collection endpoints to fetch and persist Azure data:

```bash
curl http://localhost:8000/get-costs
curl http://localhost:8000/get-resource-utilization
curl http://localhost:8000/get-recommendations
curl http://localhost:8000/get-savings
curl http://localhost:8000/get-idle-resources
```

5. Inspect the SQLite DB file `cloud_cost_optimizer.db` or export CSV via the Power BI helper: `dashboard/powerbi/data_prep.py`.


## Detailed Usage Flow
- The FastAPI endpoints act as simple controllers. When `/get-resource-utilization` or `/get-costs` is called, `AzureDataFetcher` queries Azure (resources, metrics, cost) using `DefaultAzureCredential` and writes normalized rows into SQL tables via `database/repository.py`.
- `OptimizationEngine` reads the latest metrics and cost rows and applies rule-based functions to produce `Recommendation` rows and `SavingsEstimate` rows.
- Use the `/get-recommendations` and `/get-savings` endpoints to fetch results stored in the DB.
- The CSV created by `dashboard/powerbi/data_prep.py` is ready to ingest by Power BI Desktop/Service for visualizations.


## Where to Use (Recommended Scenarios)
- Organizations wanting a low-effort assessment of Azure spending by identifying obvious waste.
- Research projects evaluating cloud cost reduction strategies or comparing rule-based vs ML-based approaches.
- Small and medium enterprises (SMEs) without centralized cloud governance tooling seeking quick insights.
- Dev/Test environments where non-production VMs often run continuously and are good candidates for scheduling/shutdown.
- Managed Service Providers (MSPs) performing audits across customer subscriptions (with appropriate adaptation for multiple subscriptions).


## Limitations and Known Constraints
1. Data and Permissions
   - Requires a service principal or authenticated `az login` with `Cost Management Reader` and `Monitoring Reader` (or broader) permissions. Without sufficient permissions, cost and metrics queries will fail.

2. Cost Estimation Accuracy
   - The current savings estimator is heuristic and conservative. It applies simple multipliers to total cost for underutilized resources and does not perform SKU-level pricing simulations, reserved instance analysis, or sustained-use discounts.
   - It does not account for dependencies (e.g., shutting down a VM might require other services to remain available) or licensing costs.

3. Rule-based Approach
   - The optimizer uses deterministic rules (CPU threshold, unattached disks, naming conventions). It will miss complex waste patterns that could be discovered by machine learning or deeper telemetry correlation.

4. Data Freshness & API Limits
   - Azure APIs have rate limits and may return aggregated metrics with latency. The collector uses a 7–30 day lookback in examples; real-time or second-by-second telemetry is out-of-scope.

5. Single-subscription by default
   - The implementation assumes a single subscription by default (`AZURE_SUBSCRIPTION_ID`). To support enterprise multi-subscription setups, add orchestration to iterate across subscriptions and consolidate results.

6. Security & Secrets
   - Current development setup uses `.env` or local environment variables. For production, use Azure Key Vault and managed identities to avoid credential leakage.

7. Scaling & High Availability
   - SQLite is for quick testing only. For production, migrate to PostgreSQL, Azure SQL, or another enterprise database and run collectors as scheduled workers (Celery/APS/cron) behind durable task queues.

8. Automation & Remediation
   - The project currently provides recommendations but does not perform automated remediation. Automated actions must be designed with approval workflows and safe rollback mechanisms.


## Integration Points and Extensibility
- Power BI: Use `dashboard/powerbi/data_prep.py` to export CSV for reporting. For automated reporting, integrate with Power BI REST API.
- CI/CD: The repository includes a GitHub Actions workflow that runs tests and builds an image; add ACR push and AKS deployment steps to enable automatic deployment.
- Secrets: Integrate Azure Key Vault and GitHub Secrets for secure deployment.
- Scheduler: Add APScheduler/Cron or Celery workers to run `AzureDataFetcher` at intervals (hourly/daily) and persist historical metrics.
- Multi-cloud: Add AWS/GCP collectors to build cross-cloud optimization insights.


## Metrics to Track (Success Criteria)
- Number of idle or underutilized resources identified per month.
- Estimated vs actual cost savings after applying recommendations (validated monthly).
- Reduction in overall monthly cloud spend percentage.
- Time-to-detect from when a resource becomes idle to when it is reported by CCOS.


## Production Recommendations
- Replace SQLite with Azure SQL or PostgreSQL and set `DATABASE_URL`.
- Use managed identities or Key Vault for credentials; disable long-lived SP secrets where possible.
- Run collector as scheduled job in Kubernetes (CronJob) or via serverless functions for smaller footprints.
- Add logging (structured logs) and monitoring for collector failures and API health (use Application Insights or Prometheus + Grafana).
- Implement multi-tenant/multi-subscription orchestration if auditing many subscriptions.


## Next Steps (Suggested Enhancements)
1. Add automated remediation with approval flow (e.g., create Azure Automation runbooks or GitHub actions that require human confirmation). 
2. Add machine learning-based rightsizing suggestions trained on historical utilization patterns.
3. Implement RBAC and an administrative UI to approve and apply actions.
4. Add cost-modeling for reserved instances, spot instances, and sustained-use discounts.


## References
- Azure Cost Management REST API
- Azure Monitor Metrics
- Power BI Desktop and Power BI REST API


---
Document created: `docs/USAGE_LIMITATIONS.md`
