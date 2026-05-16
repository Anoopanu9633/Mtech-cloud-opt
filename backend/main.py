from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import init_db, get_db
from collector.data_fetcher import AzureDataFetcher
from optimizer.engine import OptimizationEngine
from database.repository import (
    get_latest_cost_records,
    get_latest_resource_metrics,
    get_latest_recommendations,
    get_latest_savings,
    get_idle_resources,
)

app = FastAPI(
    title="Cloud Cost Optimization System",
    description="Azure cost and resource optimization API for cloud monitoring and savings recommendations.",
    version="1.0.0",
)

init_db()

fetcher = AzureDataFetcher()
engine = OptimizationEngine()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/get-costs")
def get_costs(db: Session = Depends(get_db)):
    try:
        cost_records = fetcher.fetch_cost_records(db)
        return {"cost_records": cost_records}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/get-resource-utilization")
def get_resource_utilization(db: Session = Depends(get_db)):
    try:
        metrics = fetcher.fetch_resource_metrics(db)
        return {"resource_metrics": metrics}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/get-recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    try:
        recommendations = engine.generate_recommendations(db)
        return {"recommendations": recommendations}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/get-savings")
def get_savings(db: Session = Depends(get_db)):
    try:
        savings = engine.estimate_savings(db)
        return {"savings": savings}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/get-idle-resources")
def get_idle_resources(db: Session = Depends(get_db)):
    try:
        idle_resources = get_idle_resources(db)
        return {"idle_resources": idle_resources}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
