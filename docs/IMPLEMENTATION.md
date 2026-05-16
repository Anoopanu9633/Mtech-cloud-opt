# Implementation Steps

## 1. Clone and prepare the repository

- Clone the repository to your local machine.
- Install Python 3.11+.
- Create a `.env` file with Azure credentials and subscription values.

## 2. Install project dependencies

```bash
python -m pip install -r requirements.txt
```

## 3. Configure Azure credentials

Set these environment variables:

- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_SUBSCRIPTION_ID`

The project uses `DefaultAzureCredential` from the Azure Identity library.

## 4. Run the FastAPI application

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 5. Validate the REST API

Open the Swagger UI at:

```
http://localhost:8000/docs
```

Key endpoints:

- `/get-costs`
- `/get-resource-utilization`
- `/get-recommendations`
- `/get-savings`
- `/get-idle-resources`

## 6. Collect Azure data

Each endpoint triggers Azure data collection and writes records to SQLite.

## 7. Review recommendations

The optimizer applies rule-based logic to detect:

- low-CPU VMs
- unattached disks
- non-production workloads running outside office hours

## 8. Prepare Power BI dashboard data

Use `dashboard/powerbi/data_prep.py` to generate a CSV export for Power BI.

## 9. Dockerize the application

Build and run with:

```bash
docker build -t cloud-cost-optimizer .
docker run --rm -p 8000:8000 --env-file .env cloud-cost-optimizer
```

## 10. CI/CD with GitHub Actions

The workflow defined in `.github/workflows/ci-cd.yml`:

- installs dependencies
- runs tests
- performs static syntax validation
- builds the Docker image

## 11. Optional Kubernetes deployment

Use the manifests in `k8s/` to deploy to AKS or any Kubernetes cluster.

- `k8s/deployment.yaml`
- `k8s/service.yaml`
