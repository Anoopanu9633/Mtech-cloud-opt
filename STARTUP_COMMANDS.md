# 🚀 Cloud Cost Optimizer - Quick Start Commands

Complete reference for starting and managing the Cloud Cost Optimization System.

---

## ⚡ Quick Start (5 minutes)

### Windows (PowerShell)
```powershell
# 1. Add Azure CLI to PATH
$env:Path += ";C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin"

# 2. Load environment
Get-Content .env | ForEach-Object { [Environment]::SetEnvironmentVariable($_.Split('=')[0], $_.Split('=')[1]) }

# 3. Login to Azure
az login --service-principal -u $env:AZURE_CLIENT_ID -p $env:AZURE_CLIENT_SECRET --tenant $env:AZURE_TENANT_ID

# 4. Set subscription
az account set --subscription $env:AZURE_SUBSCRIPTION_ID

# 5. Start server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 6. In another terminal - export data
python export_data.py

# 7. Test
curl http://localhost:8000/health
```

### Linux/Mac (Bash)
```bash
# 1. Load environment
source .env

# 2. Login to Azure
az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID

# 3. Set subscription
az account set --subscription $AZURE_SUBSCRIPTION_ID

# 4. Start server
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 5. In another terminal - export data
python3 export_data.py

# 6. Test
curl http://localhost:8000/health
```

---

## 📋 Command Reference

### 1️⃣ Prerequisites

| Command | Purpose |
|---------|---------|
| `python --version` | Check Python version (requires 3.14+) |
| `az --version` | Check Azure CLI (requires 2.87.0+) |
| `docker --version` | Verify Docker installation |
| `git --version` | Check git installation |

### 2️⃣ Environment Setup

| Command | Purpose |
|---------|---------|
| `Copy-Item .env.example .env` | Copy template (Windows) |
| `cp .env.example .env` | Copy template (Linux/Mac) |
| `notepad .env` | Edit on Windows |
| `nano .env` | Edit on Linux/Mac |

**Required .env Variables:**
```
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

### 3️⃣ Azure Authentication

| Command | Purpose |
|---------|---------|
| `az login --service-principal -u $CLIENT_ID -p $SECRET --tenant $TENANT` | Authenticate to Azure |
| `az account set --subscription $SUBSCRIPTION_ID` | Set active subscription |
| `az account show` | Verify subscription access |
| `az role assignment list --assignee $CLIENT_ID` | Check role assignments |
| `az resource list --subscription $SUBSCRIPTION_ID` | List Azure resources |

### 4️⃣ FastAPI Server

| Command | Purpose |
|---------|---------|
| `python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000` | Start dev server |
| `curl http://localhost:8000/docs` | Access API documentation |
| `curl http://localhost:8000/redoc` | Access ReDoc documentation |

**Access Points:**
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5️⃣ API Endpoints

| Endpoint | Command | Purpose |
|----------|---------|---------|
| `/health` | `curl http://localhost:8000/health` | Health check |
| `/get-costs` | `curl http://localhost:8000/get-costs` | Get cost data |
| `/get-resource-utilization` | `curl http://localhost:8000/get-resource-utilization` | Resource metrics |
| `/get-recommendations` | `curl http://localhost:8000/get-recommendations` | Optimization recommendations |
| `/get-savings` | `curl http://localhost:8000/get-savings` | Savings estimation |
| `/get-idle-resources` | `curl http://localhost:8000/get-idle-resources` | Idle resources |

### 6️⃣ Database Operations

| Command | Purpose |
|---------|---------|
| `python verify_db.py` | Check database tables and records |
| `python export_data.py` | Export data to CSV (for Power BI) |
| `sqlite3 cloud_cost_optimizer.db` | Open database directly |
| `ls -la exports/` | List exported CSV files |

**Database Files:**
- SQLite: `cloud_cost_optimizer.db` (40 KB)
- CSV Export Directory: `exports/`
  - `resource_metrics.csv`
  - `cost_records.csv`
  - `recommendations.csv`
  - `savings_estimates.csv`

### 7️⃣ Testing

| Command | Purpose |
|---------|---------|
| `python -m pytest -v` | Run all tests |
| `python -m pytest tests/test_app.py -v` | Run specific test |
| `python -m pytest --cov=backend tests/` | Run with coverage |
| `python -m py_compile backend/main.py` | Check syntax |

### 8️⃣ Docker Commands

| Command | Purpose |
|---------|---------|
| `docker build -t cloud-cost-optimizer:latest .` | Build Docker image |
| `docker-compose -f docker/docker-compose.yml up -d` | Start with Docker Compose |
| `docker-compose -f docker/docker-compose.yml ps` | View running containers |
| `docker-compose -f docker/docker-compose.yml logs -f` | View logs |
| `docker-compose -f docker/docker-compose.yml down` | Stop containers |

### 9️⃣ Git Commands

| Command | Purpose |
|---------|---------|
| `git status` | Check repository status |
| `git log --oneline -10` | View recent commits |
| `git add -A` | Stage all changes |
| `git commit -m "message"` | Commit changes |
| `git push origin main` | Push to GitHub |

### 🔟 Kubernetes (Optional)

| Command | Purpose |
|---------|---------|
| `kubectl create configmap cloud-cost-optimizer --from-env-file=.env` | Create config |
| `kubectl apply -f k8s/deployment.yaml` | Deploy to Kubernetes |
| `kubectl get deployments -l app=cloud-cost-optimizer` | Check deployment |
| `kubectl logs -l app=cloud-cost-optimizer -f` | View pod logs |
| `kubectl port-forward svc/cloud-cost-optimizer 8000:8000` | Local port forwarding |

---

## 📂 Project Structure

```
Cloud Optimization/
├── backend/                 # FastAPI application
│   └── main.py             # Entry point
├── collector/              # Azure data collection
│   ├── azure_client.py     # Azure SDK wrapper
│   └── data_fetcher.py     # Data collection logic
├── optimizer/              # Optimization engine
│   └── engine.py           # Rule-based recommendations
├── database/               # Data persistence
│   ├── db.py              # SQLAlchemy setup
│   ├── models.py          # ORM models
│   └── repository.py      # Data repository
├── docker/                 # Containerization
│   └── docker-compose.yml # Multi-container setup
├── k8s/                    # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
├── tests/                  # Unit tests
├── exports/                # CSV exports (created at runtime)
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Template for .env
├── cloud_cost_optimizer.db # SQLite database (created at runtime)
└── requirements.txt        # Python dependencies
```

---

## 🔐 Security Notes

⚠️ **CRITICAL: Exposed Secrets**
- Your Azure client secret was visible in the chat
- **Must rotate immediately**:
  1. Azure Portal → App registrations → cloud-cost-optimizer-sp
  2. Certificates & secrets → Delete old secret
  3. Create new secret
  4. Update `.env` file

✅ **Best Practices:**
- Never commit `.env` file (already in `.gitignore`)
- Store secrets in Azure Key Vault for production
- Use GitHub Secrets for CI/CD
- Rotate credentials regularly

---

## 🐛 Troubleshooting

### Azure CLI not recognized
```powershell
# Add to PATH permanently
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin", [EnvironmentVariableTarget]::User)
```

### Port 8000 already in use
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac: Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Database locked
```bash
# Verify no other processes have the database open
lsof | grep cloud_cost_optimizer.db
```

### Azure authentication fails
- Verify credentials in `.env` are correct
- Ensure service principal has required roles:
  - Cost Management Reader
  - Monitoring Reader
  - Reader

---

## 📖 Documentation

- **README.md** - Project overview
- **docs/MTECH_PROJECT_REPORT.md** - Full M.Tech report (28 sections)
- **docs/ABSTRACT.md** - Executive summary
- **docs/USAGE_LIMITATIONS.md** - Usage guide and limitations
- **startup-commands.ps1** - Interactive Windows startup guide
- **startup-commands.sh** - Interactive Linux/Mac startup guide

---

## 🔗 Links

- **GitHub Repository**: https://github.com/Anoopanu9633/Mtech-cloud-opt
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Azure SDK Documentation**: https://learn.microsoft.com/en-us/azure/developer/python/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/

---

## ✅ Verification Checklist

- [ ] Python 3.14+ installed
- [ ] Azure CLI 2.87.0+ installed
- [ ] `.env` file configured with Azure credentials
- [ ] Azure service principal authenticated
- [ ] FastAPI server starts on port 8000
- [ ] Health endpoint responds: `http://localhost:8000/health`
- [ ] Database created: `cloud_cost_optimizer.db`
- [ ] CSV exports generated in `exports/` directory
- [ ] All tests passing: `pytest -v`
- [ ] Git repository configured and pushed to GitHub

---

**Last Updated**: 2026-06-12  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
