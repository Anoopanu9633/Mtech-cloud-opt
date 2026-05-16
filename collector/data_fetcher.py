import os
from datetime import datetime
from azure.core.exceptions import HttpResponseError

from collector.azure_client import query_cost_data, query_metrics, query_resource_list, get_resource_status
from database.repository import save_cost_records, save_resource_metrics


class AzureDataFetcher:
    def __init__(self):
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

    def _build_resource_metric(self, resource, metrics):
        return {
            "resource_id": resource.id,
            "resource_name": getattr(resource, "name", "unknown"),
            "resource_type": getattr(resource, "type", "unknown"),
            "subscription_id": self.subscription_id,
            "region": getattr(resource, "location", "unknown"),
            "cpu_utilization": metrics.get("Percentage CPU", metrics.get("CPU Percentage", 0.0)),
            "disk_read_bytes": metrics.get("Disk Read Bytes", 0.0),
            "disk_write_bytes": metrics.get("Disk Write Bytes", 0.0),
            "storage_used_gb": metrics.get("Used Capacity", 0.0),
            "status": get_resource_status(resource),
        }

    def fetch_resources(self):
        resources = query_resource_list()
        return resources

    def fetch_resource_metrics(self, db):
        resources = self.fetch_resources()
        records = []
        for resource in resources:
            try:
                metrics = query_metrics(
                    resource.id,
                    metric_names=["Percentage CPU", "CPU Percentage", "Used Capacity", "Disk Read Bytes", "Disk Write Bytes"],
                )
            except HttpResponseError:
                metrics = {}

            resource_metric = self._build_resource_metric(resource, metrics)
            records.append(resource_metric)

        saved = save_resource_metrics(db, records)
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
            for record in saved
        ]

    def fetch_cost_records(self, db):
        costs = query_cost_data()
        saved = save_cost_records(db, costs)
        return [
            {
                "service_name": record.service_name,
                "cost_amount": record.cost_amount,
                "currency": record.currency,
                "period_start": record.period_start.isoformat(),
                "period_end": record.period_end.isoformat(),
            }
            for record in saved
        ]
