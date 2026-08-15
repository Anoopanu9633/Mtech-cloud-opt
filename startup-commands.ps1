#!/usr/bin/env powershell
<#
.SYNOPSIS
    Cloud Cost Optimizer - Complete Startup Guide
    
.DESCRIPTION
    This file contains exact commands for starting all components of the
    Cloud Cost Optimization System using Microsoft Azure.
    
.EXAMPLE
    .\startup-commands.ps1
    
.NOTES
    Prerequisites:
    - Python 3.14+ installed
    - Azure CLI 2.87.0+ installed
    - Docker Desktop installed (for container commands)
    - Virtual environment activated or dependencies installed
#>

Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║   CLOUD COST OPTIMIZER - STARTUP COMMANDS                      ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Color functions
function Write-Section { param([string]$Title)
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

function Write-Command { param([string]$Desc, [string]$Cmd)
    Write-Host "`n  📝 $Desc" -ForegroundColor Green
    Write-Host "     " -NoNewline
    Write-Host $Cmd -ForegroundColor White -BackgroundColor Black
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: PREREQUISITES & SETUP
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "1️⃣  PREREQUISITES & SETUP"

Write-Command "Check Python version" `
    "python --version"

Write-Command "Check Azure CLI installation" `
    "az --version"

Write-Command "Add Azure CLI to PATH (if needed)" `
    "`$env:Path += ';C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin'"

Write-Command "Verify git is installed" `
    "git --version"

Write-Command "Verify Docker is running" `
    "docker --version"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: ENVIRONMENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "2️⃣  ENVIRONMENT CONFIGURATION"

Write-Command "Copy environment template" `
    "Copy-Item .env.example .env"

Write-Command "Edit environment file with your credentials" `
    "notepad .env"

Write-Host "`n  ⚠️  REQUIRED in .env file:" -ForegroundColor Magenta
Write-Host "     - AZURE_TENANT_ID" -ForegroundColor Gray
Write-Host "     - AZURE_CLIENT_ID" -ForegroundColor Gray
Write-Host "     - AZURE_CLIENT_SECRET" -ForegroundColor Gray
Write-Host "     - AZURE_SUBSCRIPTION_ID" -ForegroundColor Gray

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: AZURE CLI AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "3️⃣  AZURE CLI AUTHENTICATION"

Write-Command "Login with service principal" `
    "az login --service-principal -u `$env:AZURE_CLIENT_ID -p `$env:AZURE_CLIENT_SECRET --tenant `$env:AZURE_TENANT_ID"

Write-Command "Set active subscription" `
    "az account set --subscription `$env:AZURE_SUBSCRIPTION_ID"

Write-Command "Verify subscription access" `
    "az account show"

Write-Command "List role assignments" `
    "az role assignment list --assignee `$env:AZURE_CLIENT_ID --subscription `$env:AZURE_SUBSCRIPTION_ID --output table"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: LOCAL DEVELOPMENT SERVER
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "4️⃣  LOCAL DEVELOPMENT SERVER (FastAPI)"

Write-Command "Start FastAPI development server" `
    "python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "`n  ✨ Once running, access:" -ForegroundColor Cyan
Write-Host "     • API:       http://localhost:8000" -ForegroundColor Gray
Write-Host "     • Docs:      http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "     • ReDoc:     http://localhost:8000/redoc" -ForegroundColor Gray

Write-Command "Health check (in another terminal)" `
    "curl http://localhost:8000/health"

Write-Command "Get resources" `
    "curl http://localhost:8000/get-resource-utilization"

Write-Command "Get recommendations" `
    "curl http://localhost:8000/get-recommendations"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: DOCKER & CONTAINERIZATION
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "5️⃣  DOCKER & CONTAINERIZATION"

Write-Command "Build Docker image" `
    "docker build -t cloud-cost-optimizer:latest ."

Write-Command "Start with Docker Compose" `
    "docker-compose -f docker/docker-compose.yml up -d"

Write-Command "View running containers" `
    "docker-compose -f docker/docker-compose.yml ps"

Write-Command "Stop Docker Compose services" `
    "docker-compose -f docker/docker-compose.yml down"

Write-Command "View container logs" `
    "docker-compose -f docker/docker-compose.yml logs -f"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: DATABASE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "6️⃣  DATABASE OPERATIONS"

Write-Command "Verify database tables and records" `
    "python verify_db.py"

Write-Command "Export data to CSV (for Power BI)" `
    "python export_data.py"

Write-Command "View exported CSV files" `
    "Get-ChildItem exports/*.csv | Format-Table Name, Length"

Write-Command "Open database with SQLite" `
    "sqlite3 cloud_cost_optimizer.db"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: TESTING
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "7️⃣  TESTING"

Write-Command "Run all tests" `
    "python -m pytest -v"

Write-Command "Run specific test file" `
    "python -m pytest tests/test_app.py -v"

Write-Command "Run with coverage" `
    "python -m pytest --cov=backend --cov=collector --cov=optimizer tests/"

Write-Command "Check Python syntax" `
    "python -m py_compile backend/main.py collector/azure_client.py optimizer/engine.py"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: API ENDPOINTS - QUICK TEST
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "8️⃣  API ENDPOINTS - QUICK TEST"

Write-Host "`n  🔗 Test all endpoints (after server is running):" -ForegroundColor Yellow

Write-Command "Health Check" `
    "curl http://localhost:8000/health"

Write-Command "Get Costs" `
    "curl http://localhost:8000/get-costs"

Write-Command "Get Resource Utilization" `
    "curl http://localhost:8000/get-resource-utilization"

Write-Command "Get Recommendations" `
    "curl http://localhost:8000/get-recommendations"

Write-Command "Get Savings" `
    "curl http://localhost:8000/get-savings"

Write-Command "Get Idle Resources" `
    "curl http://localhost:8000/get-idle-resources"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: GIT & VERSION CONTROL
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "9️⃣  GIT & VERSION CONTROL"

Write-Command "Check git status" `
    "git status"

Write-Command "View commit history" `
    "git log --oneline -10"

Write-Command "Stage all changes" `
    "git add -A"

Write-Command "Commit changes" `
    "git commit -m 'Your commit message'"

Write-Command "Push to GitHub" `
    "git push origin main"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: KUBERNETES DEPLOYMENT (Optional)
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "🔟 KUBERNETES DEPLOYMENT (Optional)"

Write-Command "Create ConfigMap for .env" `
    "kubectl create configmap cloud-cost-optimizer --from-env-file=.env"

Write-Command "Apply Kubernetes manifests" `
    "kubectl apply -f k8s/deployment.yaml"

Write-Command "Apply service" `
    "kubectl apply -f k8s/service.yaml"

Write-Command "Check deployment status" `
    "kubectl get deployments -l app=cloud-cost-optimizer"

Write-Command "View pod logs" `
    "kubectl logs -l app=cloud-cost-optimizer -f"

Write-Command "Port forward to local" `
    "kubectl port-forward svc/cloud-cost-optimizer 8000:8000"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11: COMPLETE STARTUP WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════

Write-Section "1️⃣1️⃣  COMPLETE STARTUP WORKFLOW"

Write-Host "`n  🚀 Run these commands in order to start everything:" -ForegroundColor Green

Write-Host "`n  1. Add Azure CLI to PATH:" -ForegroundColor Cyan
Write-Host "     `$env:Path += ';C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin'" -ForegroundColor White

Write-Host "`n  2. Azure Authentication:" -ForegroundColor Cyan
Write-Host "     az login --service-principal -u `$env:AZURE_CLIENT_ID -p `$env:AZURE_CLIENT_SECRET --tenant `$env:AZURE_TENANT_ID" -ForegroundColor White

Write-Host "`n  3. Set Subscription:" -ForegroundColor Cyan
Write-Host "     az account set --subscription `$env:AZURE_SUBSCRIPTION_ID" -ForegroundColor White

Write-Host "`n  4. Start FastAPI Server:" -ForegroundColor Cyan
Write-Host "     python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White

Write-Host "`n  5. In Another Terminal - Export Data:" -ForegroundColor Cyan
Write-Host "     python export_data.py" -ForegroundColor White

Write-Host "`n  6. Test Endpoints:" -ForegroundColor Cyan
Write-Host "     curl http://localhost:8000/health" -ForegroundColor White

# ═══════════════════════════════════════════════════════════════════════════════
# CLOSING
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔════════════════════════════════════════════════════════════════╗"
Write-Host "║                     ✅ SETUP COMPLETE                          ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "   • README.md - Project overview" -ForegroundColor Gray
Write-Host "   • docs/MTECH_PROJECT_REPORT.md - Detailed report" -ForegroundColor Gray
Write-Host "   • docs/USAGE_LIMITATIONS.md - Usage guide" -ForegroundColor Gray

Write-Host "`n📊 Data Files:" -ForegroundColor Yellow
Write-Host "   • cloud_cost_optimizer.db - SQLite database" -ForegroundColor Gray
Write-Host "   • exports/ - CSV files for Power BI" -ForegroundColor Gray

Write-Host "`n🔗 GitHub:" -ForegroundColor Yellow
Write-Host "   https://github.com/Anoopanu9633/Mtech-cloud-opt" -ForegroundColor Gray

Write-Host ""
