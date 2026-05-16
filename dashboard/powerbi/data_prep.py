import csv
from datetime import datetime

SAMPLE_REPORT_PATH = "dashboard/powerbi/sample_export.csv"


def generate_sample_report(cost_rows, metric_rows, recommendation_rows):
    with open(SAMPLE_REPORT_PATH, mode="w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow([
            "report_generated_at",
            "category",
            "resource_name",
            "metric",
            "value",
            "currency",
            "estimated_savings",
        ])
        timestamp = datetime.utcnow().isoformat()
        for row in cost_rows:
            writer.writerow([
                timestamp,
                "cost",
                row.get("service_name"),
                "daily_cost",
                row.get("cost_amount"),
                row.get("currency"),
                "",
            ])
        for row in metric_rows:
            writer.writerow([
                timestamp,
                "utilization",
                row.get("resource_name"),
                "cpu_utilization",
                row.get("cpu_utilization"),
                "",
                "",
            ])
        for row in recommendation_rows:
            writer.writerow([
                timestamp,
                "recommendation",
                row.get("resource_name"),
                row.get("recommendation_type"),
                row.get("estimated_monthly_savings"),
                "",
                row.get("estimated_monthly_savings"),
            ])


if __name__ == "__main__":
    sample_cost_rows = [
        {"service_name": "Virtual Machines", "cost_amount": 430.0, "currency": "USD"},
    ]
    sample_metric_rows = [
        {"resource_name": "dev-vm-01", "cpu_utilization": 6.5},
    ]
    sample_recommendations = [
        {"resource_name": "dev-vm-01", "recommendation_type": "CPU Underutilized", "estimated_monthly_savings": 25.0},
    ]
    generate_sample_report(sample_cost_rows, sample_metric_rows, sample_recommendations)
    print(f"Sample Power BI CSV export created at {SAMPLE_REPORT_PATH}")
