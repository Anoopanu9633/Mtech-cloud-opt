import os

from collector.azure_client import get_resource_status, query_cost_data, query_metrics, query_resource_list
from database.repository import save_cost_records, save_resource_metrics


class AzureDataFetcher:
    def __init__(self):
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

    def _get_metric_names_for_resource(self, resource):
        resource_type = getattr(resource, "type", "").lower()
        if "microsoft.storage/storageaccounts" in resource_type:
            return ["UsedCapacity"]
        if "microsoft.compute/virtualmachines" in resource_type:
            return ["Percentage CPU", "Disk Read Bytes", "Disk Write Bytes"]
        return []

    def _build_resource_metric(self, resource, metrics):
        resource_type = getattr(resource, "type", "").lower()
        is_storage_account = "microsoft.storage/storageaccounts" in resource_type
        cpu_value = None if is_storage_account else metrics.get("Percentage CPU")

        return {
            "resource_id": resource.id,
            "resource_name": getattr(resource, "name", "unknown"),
            "resource_type": getattr(resource, "type", "unknown"),
            "subscription_id": self.subscription_id,
            "region": getattr(resource, "location", "unknown"),
            "cpu_utilization": cpu_value,
            "disk_read_bytes": metrics.get("Disk Read Bytes", 0.0),
            "disk_write_bytes": metrics.get("Disk Write Bytes", 0.0),
            "storage_used_gb": metrics.get("UsedCapacity", metrics.get("Used Capacity", 0.0)),
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
                metric_names = self._get_metric_names_for_resource(resource)
                metrics = query_metrics(resource.id, metric_names=metric_names)
            except Exception:
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
