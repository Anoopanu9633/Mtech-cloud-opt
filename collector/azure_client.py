import os
from datetime import datetime, timedelta

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.monitor.query import MetricsQueryClient


def get_credentials():
    return DefaultAzureCredential()


def get_subscription_id():
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is required")
    return subscription_id


def build_cost_client():
    credential = get_credentials()
    return CostManagementClient(credential, get_subscription_id())


def build_resource_client():
    credential = get_credentials()
    return ResourceManagementClient(credential, get_subscription_id())


def build_metrics_client():
    credential = get_credentials()
    return MetricsQueryClient(credential)


def query_resource_list():
    client = build_resource_client()
    return list(client.resources.list())


def query_cost_data(scope: str = None):
    client = build_cost_client()
    if scope is None:
        scope = f"/subscriptions/{get_subscription_id()}"
    end = datetime.utcnow().date()
    start = end - timedelta(days=30)
    query = {
        "type": "ActualCost",
        "timeframe": "Custom",
        "timePeriod": {
            "from": start.isoformat(),
            "to": end.isoformat(),
        },
        "dataset": {
            "granularity": "Daily",
            "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}],
        },
    }
    try:
        response = client.query.usage(scope=scope, parameters=query)
        rows = []
        if response and response.properties and response.properties.rows:
            for row in response.properties.rows:
                service_name = row[0]
                cost_amount = float(row[1]) if row[1] is not None else 0.0
                rows.append(
                    {
                        "subscription_id": get_subscription_id(),
                        "service_name": service_name,
                        "cost_amount": cost_amount,
                        "currency": response.properties.currency,
                        "period_start": start,
                        "period_end": end,
                    }
                )
        return rows
    except Exception as e:
        # Handle Azure SDK deserialization errors gracefully
        print(f"Warning: Failed to fetch cost data: {e}")
        return []


def query_metrics(resource_id: str, metric_names: list[str], timespan=None, interval="PT1H"):
    client = build_metrics_client()
    if timespan is None:
        timespan = timedelta(days=7)
    try:
        result = client.query_resource(
            resource_id,
            metric_names=metric_names,
            timespan=timespan,
            interval=interval,
            aggregations=["Average"],
        )
        metrics = {}
        for metric in result.metrics:
            if not metric.timeseries:
                continue
            series = metric.timeseries[0]
            values = [point.average for point in series.data if point.average is not None]
            metrics[metric.name.localized_value] = sum(values) / len(values) if values else 0.0
        return metrics
    except Exception as e:
        # Handle Azure SDK errors gracefully
        print(f"Warning: Failed to fetch metrics for {resource_id}: {e}")
        return {}


def get_resource_status(resource):
    properties = getattr(resource, "properties", {}) or {}
    status = properties.get("provisioningState") or properties.get("state") or "unknown"
    return status
