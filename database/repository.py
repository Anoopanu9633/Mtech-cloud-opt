from datetime import datetime
from sqlalchemy.orm import Session

from database.models import CostRecord, Recommendation, ResourceMetric, SavingsEstimate


def save_resource_metrics(db: Session, metrics):
    result = []
    for item in metrics:
        record = ResourceMetric(
            resource_id=item.get("resource_id"),
            resource_name=item.get("resource_name", "unknown"),
            resource_type=item.get("resource_type", "unknown"),
            subscription_id=item.get("subscription_id"),
            region=item.get("region"),
            cpu_utilization=item.get("cpu_utilization"),
            disk_read_bytes=item.get("disk_read_bytes"),
            disk_write_bytes=item.get("disk_write_bytes"),
            storage_used_gb=item.get("storage_used_gb"),
            status=item.get("status"),
        )
        db.add(record)
        result.append(record)
    db.commit()
    return result


def save_cost_records(db: Session, costs):
    result = []
    for item in costs:
        record = CostRecord(
            subscription_id=item.get("subscription_id"),
            service_name=item.get("service_name"),
            cost_amount=item.get("cost_amount", 0.0),
            currency=item.get("currency", "USD"),
            period_start=item.get("period_start", datetime.utcnow()),
            period_end=item.get("period_end", datetime.utcnow()),
        )
        db.add(record)
        result.append(record)
    db.commit()
    return result


def save_recommendations(db: Session, recommendations):
    result = []
    for item in recommendations:
        record = Recommendation(
            resource_id=item.get("resource_id"),
            resource_name=item.get("resource_name"),
            recommendation_type=item.get("recommendation_type"),
            message=item.get("message"),
            estimated_monthly_savings=item.get("estimated_monthly_savings", 0.0),
        )
        db.add(record)
        result.append(record)
    db.commit()
    return result


def save_savings_estimate(db: Session, estimate):
    record = SavingsEstimate(
        total_current_monthly_cost=estimate.get("total_current_monthly_cost", 0.0),
        estimated_optimized_monthly_cost=estimate.get("estimated_optimized_monthly_cost", 0.0),
        estimated_monthly_savings=estimate.get("estimated_monthly_savings", 0.0),
    )
    db.add(record)
    db.commit()
    return record


def get_latest_cost_records(db: Session, limit: int = 20):
    return [
        {
            "service_name": record.service_name,
            "cost_amount": record.cost_amount,
            "currency": record.currency,
            "period_start": record.period_start.isoformat(),
            "period_end": record.period_end.isoformat(),
        }
        for record in db.query(CostRecord).order_by(CostRecord.timestamp.desc()).limit(limit)
    ]


def get_latest_resource_metrics(db: Session, limit: int = 50):
    return [
        {
            "resource_id": record.resource_id,
            "resource_name": record.resource_name,
            "resource_type": record.resource_type,
            "cpu_utilization": record.cpu_utilization,
            "storage_used_gb": record.storage_used_gb,
            "status": record.status,
            "timestamp": record.timestamp.isoformat(),
        }
        for record in db.query(ResourceMetric).order_by(ResourceMetric.timestamp.desc()).limit(limit)
    ]


def get_latest_recommendations(db: Session, limit: int = 50):
    return [
        {
            "resource_id": record.resource_id,
            "resource_name": record.resource_name,
            "recommendation_type": record.recommendation_type,
            "message": record.message,
            "estimated_monthly_savings": record.estimated_monthly_savings,
            "timestamp": record.timestamp.isoformat(),
        }
        for record in db.query(Recommendation).order_by(Recommendation.timestamp.desc()).limit(limit)
    ]


def get_latest_savings(db: Session, limit: int = 10):
    return [
        {
            "total_current_monthly_cost": record.total_current_monthly_cost,
            "estimated_optimized_monthly_cost": record.estimated_optimized_monthly_cost,
            "estimated_monthly_savings": record.estimated_monthly_savings,
            "timestamp": record.timestamp.isoformat(),
        }
        for record in db.query(SavingsEstimate).order_by(SavingsEstimate.timestamp.desc()).limit(limit)
    ]


def get_idle_resources(db: Session, limit: int = 50):
    return [
        {
            "resource_id": record.resource_id,
            "resource_name": record.resource_name,
            "resource_type": record.resource_type,
            "status": record.status,
            "cpu_utilization": record.cpu_utilization,
            "timestamp": record.timestamp.isoformat(),
        }
        for record in db.query(ResourceMetric)
        .filter(ResourceMetric.cpu_utilization != None)
        .filter(ResourceMetric.cpu_utilization < 10.0)
        .order_by(ResourceMetric.timestamp.desc())
        .limit(limit)
    ]
