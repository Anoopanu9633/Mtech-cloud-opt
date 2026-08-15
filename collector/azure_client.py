import os
from datetime import datetime, timedelta

import requests
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


def get_access_token():
    credential = get_credentials()
    token = credential.get_token("https://management.azure.com/.default")
    return token.token


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
    if scope is None:
        scope = f"/subscriptions/{get_subscription_id()}"
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    query = {
        "type": "ActualCost",
        "timeframe": "Custom",
        "timePeriod": {
            "from": start.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
        },
        "dataset": {
            "granularity": "Daily",
            "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}],
        },
    }
    url = f"https://management.azure.com{scope}/providers/Microsoft.CostManagement/query?api-version=2024-08-01"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=query, timeout=60)
        response.raise_for_status()
        payload = response.json()
        properties = payload.get("properties", {}) or {}
        rows = properties.get("rows") or []
        currency = properties.get("currency", "USD")
    except Exception as e:
        print(f"Warning: Failed to fetch cost data: {e}")
        return []

    if not rows:
        return []

    parsed_rows = []
    for row in rows:
        if not row:
            continue
        service_name = row[0] if len(row) > 0 else "Unknown"
        cost_amount = float(row[1]) if len(row) > 1 and row[1] is not None else 0.0
        parsed_rows.append(
            {
                "subscription_id": get_subscription_id(),
                "service_name": service_name,
                "cost_amount": cost_amount,
                "currency": currency,
                "period_start": start,
                "period_end": end,
            }
        )
    return parsed_rows


def extract_metric_name(metric):
    name = getattr(metric, "name", None)
    if isinstance(name, str):
        return name
    if isinstance(name, dict):
        return name.get("localized_value") or name.get("value") or "unknown"
    if hasattr(name, "localized_value"):
        return getattr(name, "localized_value") or getattr(name, "value", "unknown")
    if hasattr(name, "value"):
        return getattr(name, "value", "unknown")
    return "unknown"


def query_metrics(resource_id: str, metric_names: list[str], timespan=None, interval=None):
    client = build_metrics_client()
    if timespan is None:
        timespan = timedelta(days=7)

    query_kwargs = {
        "metric_names": metric_names,
        "timespan": timespan,
        "aggregations": ["Average"],
    }
    if interval is not None:
        if isinstance(interval, str) and interval.endswith("H") and interval[:-1].isdigit():
            query_kwargs["granularity"] = timedelta(hours=int(interval[:-1]))
        else:
            query_kwargs["granularity"] = interval

    try:
        result = client.query_resource(resource_id, **query_kwargs)
        metrics = {}
        for metric in result.metrics:
            if not getattr(metric, "timeseries", None):
                continue
            series = metric.timeseries[0]
            values = [point.average for point in series.data if getattr(point, "average", None) is not None]
            metric_name = extract_metric_name(metric)
            if values:
                metrics[metric_name] = sum(values) / len(values)
            else:
                metrics[metric_name] = 0.0
        return metrics
    except Exception as e:
        print(f"Warning: Failed to fetch metrics for {resource_id}: {e}")
        return {}


def get_resource_status(resource):
    properties = getattr(resource, "properties", {}) or {}
    status = properties.get("provisioningState") or properties.get("state") or "unknown"
    return status
