@echo off
REM Cloud Cost Optimizer - Windows Startup Script
REM This batch file helps start the application on Windows

color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   CLOUD COST OPTIMIZER - WINDOWS STARTUP                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo.
    echo Please create .env file first:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env with your Azure credentials
    echo.
    pause
    exit /b 1
)

echo ✅ .env file found
echo.

REM Add Azure CLI to PATH
echo 📝 Setting up Azure CLI...
set PATH=%PATH%;C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin

REM Verify Azure CLI
az --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Azure CLI not found!
    echo Please install: winget install --id Microsoft.AzureCLI
    pause
    exit /b 1
)
echo ✅ Azure CLI is available
echo.

REM Load environment variables from .env
echo 📝 Loading environment variables from .env...
for /f "delims=" %%i in ('type .env ^| findstr /v "^REM"') do (
    for /f "tokens=1* delims==" %%a in ("%%i") do (
        if not "%%a"=="" set "%%i"
    )
)
echo ✅ Environment variables loaded
echo.

REM Test Azure authentication
echo 📝 Testing Azure authentication...
az account show >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Not authenticated to Azure. Attempting login...
    echo.
    echo Running: az login --service-principal -u %AZURE_CLIENT_ID% -p *** --tenant %AZURE_TENANT_ID%
    echo.
    az login --service-principal -u "%AZURE_CLIENT_ID%" -p "%AZURE_CLIENT_SECRET%" --tenant "%AZURE_TENANT_ID%"
    if errorlevel 1 (
        echo ❌ Azure authentication failed!
        pause
        exit /b 1
    )
)
echo ✅ Azure authentication successful
echo.

REM Set subscription
echo 📝 Setting subscription...
az account set --subscription "%AZURE_SUBSCRIPTION_ID%"
if errorlevel 1 (
    echo ❌ Failed to set subscription!
    pause
    exit /b 1
)
echo ✅ Subscription set: %AZURE_SUBSCRIPTION_ID%
echo.

REM Start FastAPI server
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🚀 STARTING FASTAPI SERVER                                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Server will start on: http://localhost:8000
echo Docs available at:   http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
pause

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo.
    echo ❌ FastAPI server failed to start!
    pause
    exit /b 1
)

pause
