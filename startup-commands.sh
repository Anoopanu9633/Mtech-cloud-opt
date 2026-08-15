#!/bin/bash
##############################################################################
#  Cloud Cost Optimizer - Startup Commands (Linux/Mac)
#  Complete guide for starting all components
##############################################################################

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Helper functions
section() {
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
}

command_info() {
    echo -e "\n  ${GREEN}📝 $1${NC}"
    echo -e "     ${BLUE}$2${NC}"
}

##############################################################################
# HEADER
##############################################################################

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   CLOUD COST OPTIMIZER - STARTUP COMMANDS (Linux/Mac)         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"

##############################################################################
# SECTION 1: PREREQUISITES
##############################################################################

section "1️⃣  PREREQUISITES & SETUP"

command_info "Check Python version" \
    "python3 --version"

command_info "Check Azure CLI installation" \
    "az --version"

command_info "Verify git is installed" \
    "git --version"

command_info "Verify Docker is running" \
    "docker --version"

##############################################################################
# SECTION 2: ENVIRONMENT SETUP
##############################################################################

section "2️⃣  ENVIRONMENT CONFIGURATION"

command_info "Copy environment template" \
    "cp .env.example .env"

command_info "Edit environment file with your credentials" \
    "nano .env   # or: vi .env"

echo -e "\n  ${MAGENTA}⚠️  REQUIRED in .env file:${NC}"
echo -e "     - AZURE_TENANT_ID"
echo -e "     - AZURE_CLIENT_ID"
echo -e "     - AZURE_CLIENT_SECRET"
echo -e "     - AZURE_SUBSCRIPTION_ID"

##############################################################################
# SECTION 3: AZURE CLI AUTHENTICATION
##############################################################################

section "3️⃣  AZURE CLI AUTHENTICATION"

command_info "Login with service principal" \
    "az login --service-principal -u \$AZURE_CLIENT_ID -p \$AZURE_CLIENT_SECRET --tenant \$AZURE_TENANT_ID"

command_info "Set active subscription" \
    "az account set --subscription \$AZURE_SUBSCRIPTION_ID"

command_info "Verify subscription access" \
    "az account show"

command_info "List role assignments" \
    "az role assignment list --assignee \$AZURE_CLIENT_ID --subscription \$AZURE_SUBSCRIPTION_ID --output table"

##############################################################################
# SECTION 4: LOCAL DEVELOPMENT
##############################################################################

section "4️⃣  LOCAL DEVELOPMENT SERVER (FastAPI)"

command_info "Start FastAPI development server" \
    "python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

echo -e "\n  ${CYAN}✨ Once running, access:${NC}"
echo -e "     • API:       http://localhost:8000"
echo -e "     • Docs:      http://localhost:8000/docs"
echo -e "     • ReDoc:     http://localhost:8000/redoc"

command_info "Health check (in another terminal)" \
    "curl http://localhost:8000/health"

command_info "Get resources" \
    "curl http://localhost:8000/get-resource-utilization"

command_info "Get recommendations" \
    "curl http://localhost:8000/get-recommendations"

##############################################################################
# SECTION 5: DOCKER
##############################################################################

section "5️⃣  DOCKER & CONTAINERIZATION"

command_info "Build Docker image" \
    "docker build -t cloud-cost-optimizer:latest ."

command_info "Start with Docker Compose" \
    "docker-compose -f docker/docker-compose.yml up -d"

command_info "View running containers" \
    "docker-compose -f docker/docker-compose.yml ps"

command_info "Stop Docker Compose services" \
    "docker-compose -f docker/docker-compose.yml down"

command_info "View container logs" \
    "docker-compose -f docker/docker-compose.yml logs -f"

##############################################################################
# SECTION 6: DATABASE
##############################################################################

section "6️⃣  DATABASE OPERATIONS"

command_info "Verify database tables and records" \
    "python3 verify_db.py"

command_info "Export data to CSV (for Power BI)" \
    "python3 export_data.py"

command_info "View exported CSV files" \
    "ls -lh exports/"

command_info "Open database with SQLite" \
    "sqlite3 cloud_cost_optimizer.db"

##############################################################################
# SECTION 7: TESTING
##############################################################################

section "7️⃣  TESTING"

command_info "Run all tests" \
    "python3 -m pytest -v"

command_info "Run specific test file" \
    "python3 -m pytest tests/test_app.py -v"

command_info "Run with coverage" \
    "python3 -m pytest --cov=backend --cov=collector --cov=optimizer tests/"

command_info "Check Python syntax" \
    "python3 -m py_compile backend/main.py collector/azure_client.py"

##############################################################################
# SECTION 8: API ENDPOINTS
##############################################################################

section "8️⃣  API ENDPOINTS - QUICK TEST"

echo -e "\n  ${YELLOW}🔗 Test all endpoints (after server is running):${NC}"

command_info "Health Check" \
    "curl http://localhost:8000/health"

command_info "Get Costs" \
    "curl http://localhost:8000/get-costs"

command_info "Get Resource Utilization" \
    "curl http://localhost:8000/get-resource-utilization"

command_info "Get Recommendations" \
    "curl http://localhost:8000/get-recommendations"

command_info "Get Savings" \
    "curl http://localhost:8000/get-savings"

command_info "Get Idle Resources" \
    "curl http://localhost:8000/get-idle-resources"

##############################################################################
# SECTION 9: GIT
##############################################################################

section "9️⃣  GIT & VERSION CONTROL"

command_info "Check git status" \
    "git status"

command_info "View commit history" \
    "git log --oneline -10"

command_info "Stage all changes" \
    "git add -A"

command_info "Commit changes" \
    "git commit -m 'Your commit message'"

command_info "Push to GitHub" \
    "git push origin main"

##############################################################################
# SECTION 10: KUBERNETES
##############################################################################

section "🔟 KUBERNETES DEPLOYMENT (Optional)"

command_info "Create ConfigMap for .env" \
    "kubectl create configmap cloud-cost-optimizer --from-env-file=.env"

command_info "Apply Kubernetes manifests" \
    "kubectl apply -f k8s/deployment.yaml"

command_info "Check deployment status" \
    "kubectl get deployments -l app=cloud-cost-optimizer"

command_info "View pod logs" \
    "kubectl logs -l app=cloud-cost-optimizer -f"

command_info "Port forward to local" \
    "kubectl port-forward svc/cloud-cost-optimizer 8000:8000"

##############################################################################
# SECTION 11: QUICK START
##############################################################################

section "1️⃣1️⃣  QUICK START WORKFLOW"

echo -e "\n  ${GREEN}🚀 Run these commands in order:${NC}"

echo -e "\n  ${CYAN}1. Load environment variables:${NC}"
echo -e "     source .env"

echo -e "\n  ${CYAN}2. Azure Authentication:${NC}"
echo -e "     az login --service-principal -u \$AZURE_CLIENT_ID -p \$AZURE_CLIENT_SECRET --tenant \$AZURE_TENANT_ID"

echo -e "\n  ${CYAN}3. Set Subscription:${NC}"
echo -e "     az account set --subscription \$AZURE_SUBSCRIPTION_ID"

echo -e "\n  ${CYAN}4. Start FastAPI Server:${NC}"
echo -e "     python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

echo -e "\n  ${CYAN}5. In Another Terminal - Export Data:${NC}"
echo -e "     python3 export_data.py"

echo -e "\n  ${CYAN}6. Test Endpoints:${NC}"
echo -e "     curl http://localhost:8000/health"

##############################################################################
# CLOSING
##############################################################################

echo -e "\n${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                     ✅ SETUP COMPLETE                          ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${YELLOW}📚 Documentation:${NC}"
echo -e "   • README.md - Project overview"
echo -e "   • docs/MTECH_PROJECT_REPORT.md - Detailed report"
echo -e "   • docs/USAGE_LIMITATIONS.md - Usage guide"

echo -e "\n${YELLOW}📊 Data Files:${NC}"
echo -e "   • cloud_cost_optimizer.db - SQLite database"
echo -e "   • exports/ - CSV files for Power BI"

echo -e "\n${YELLOW}🔗 GitHub:${NC}"
echo -e "   https://github.com/Anoopanu9633/Mtech-cloud-opt"

echo -e "\n"
