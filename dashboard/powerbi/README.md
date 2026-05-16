# Power BI Dashboard Preparation

This folder contains helpers for preparing Azure cost, utilization, and optimization recommendation data for Power BI.

## How to Use

1. Run the FastAPI application.
2. Export `/get-costs`, `/get-resource-utilization`, and `/get-recommendations` JSON results.
3. Use `dashboard/powerbi/data_prep.py` to build a CSV file that can be loaded into Power BI.

## Visualization Ideas

- Monthly cloud cost trend
- CPU utilization heatmap
- Idle resources map
- Optimization recommendation summary
- Estimated savings before vs after optimization
