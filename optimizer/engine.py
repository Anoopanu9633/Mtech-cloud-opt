from sqlalchemy.orm import Session

from database.models import CostRecord, ResourceMetric
from database.repository import get_latest_cost_records, get_latest_resource_metrics, save_recommendations, save_savings_estimate


class OptimizationEngine:
    def __init__(self):
        self.rules = [
            self._cpu_underutilized_rule,
            self._unattached_disk_rule,
            self._non_production_off_hours_rule,
        ]

    def _cpu_underutilized_rule(self, metric: ResourceMetric):
        if metric.cpu_utilization is not None and metric.cpu_utilization < 10.0:
            return {
                "resource_id": metric.resource_id,
                "resource_name": metric.resource_name,
                "recommendation_type": "CPU Underutilized",
                "message": "Consider shutting down or resizing this VM due to sustained low CPU utilization.",
                "estimated_monthly_savings": round((metric.cpu_utilization or 0.0) * 0.5, 2),
            }
        return None

    def _unattached_disk_rule(self, metric: ResourceMetric):
        if metric.resource_type.lower().endswith("/disks") and metric.status != "attached":
            return {
                "resource_id": metric.resource_id,
                "resource_name": metric.resource_name,
                "recommendation_type": "Unattached Disk",
                "message": "This disk appears unattached and can be deleted or archived to reduce cost.",
                "estimated_monthly_savings": 10.0,
            }
        return None

    def _non_production_off_hours_rule(self, metric: ResourceMetric):
        if "nonprod" in metric.resource_name.lower() or "dev" in metric.resource_name.lower():
            if metric.cpu_utilization is not None and metric.cpu_utilization > 0:
                return {
                    "resource_id": metric.resource_id,
                    "resource_name": metric.resource_name,
                    "recommendation_type": "Schedule Shutdown",
                    "message": "Non-production workloads should be scheduled to shut down outside office hours to save costs.",
                    "estimated_monthly_savings": 20.0,
                }
        return None

    def generate_recommendations(self, db: Session):
        metrics = db.query(ResourceMetric).order_by(ResourceMetric.timestamp.desc()).limit(200).all()
        recommendations = []
        for metric in metrics:
            for rule in self.rules:
                recommendation = rule(metric)
                if recommendation:
                    recommendations.append(recommendation)
        saved = save_recommendations(db, recommendations)
        return [
            {
                "resource_id": rec.resource_id,
                "resource_name": rec.resource_name,
                "recommendation_type": rec.recommendation_type,
                "message": rec.message,
                "estimated_monthly_savings": rec.estimated_monthly_savings,
                "timestamp": rec.timestamp.isoformat(),
            }
            for rec in saved
        ]

    def estimate_savings(self, db: Session):
        costs = db.query(CostRecord).all()
        total_cost = sum(record.cost_amount for record in costs)
        recommendations = db.query(ResourceMetric).filter(ResourceMetric.cpu_utilization != None).all()
        savings = 0.0
        for metric in recommendations:
            if metric.cpu_utilization is not None and metric.cpu_utilization < 10.0:
                savings += 0.05 * total_cost
        optimized_cost = total_cost - savings
        saved = save_savings_estimate(db, {
            "total_current_monthly_cost": total_cost,
            "estimated_optimized_monthly_cost": optimized_cost,
            "estimated_monthly_savings": savings,
        })
        return {
            "total_current_monthly_cost": saved.total_current_monthly_cost,
            "estimated_optimized_monthly_cost": saved.estimated_optimized_monthly_cost,
            "estimated_monthly_savings": saved.estimated_monthly_savings,
            "timestamp": saved.timestamp.isoformat(),
        }
