"""
Export script to generate CSV reports from the cost optimizer database
Usage: python export_data.py
Generates CSV files for Power BI visualization
"""

import csv
import os
from datetime import datetime
from pathlib import Path
import sqlite3

# Database file
DB_FILE = "cloud_cost_optimizer.db"
EXPORT_DIR = "exports"

# Create exports directory if it doesn't exist
Path(EXPORT_DIR).mkdir(exist_ok=True)

def export_resource_metrics():
    """Export resource metrics to CSV"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT resource_id, resource_name, resource_type, cpu_utilization, 
               disk_read_bytes, disk_write_bytes, storage_used_gb, status, timestamp
        FROM resource_metrics
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    csv_file = os.path.join(EXPORT_DIR, "resource_metrics.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
    
    conn.close()
    return len(rows), csv_file

def export_cost_records():
    """Export cost records to CSV"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT subscription_id, service_name, cost_amount, currency, 
               period_start, period_end, timestamp
        FROM cost_records
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    csv_file = os.path.join(EXPORT_DIR, "cost_records.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        else:
            # Write header even if no data
            writer = csv.DictWriter(f, fieldnames=[
                "subscription_id", "service_name", "cost_amount", "currency", 
                "period_start", "period_end", "timestamp"
            ])
            writer.writeheader()
    
    conn.close()
    return len(rows), csv_file

def export_recommendations():
    """Export recommendations to CSV"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT resource_id, resource_name, recommendation_type, message, 
               estimated_monthly_savings, timestamp
        FROM recommendations
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    csv_file = os.path.join(EXPORT_DIR, "recommendations.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        else:
            writer = csv.DictWriter(f, fieldnames=[
                "resource_id", "resource_name", "recommendation_type", "message", 
                "estimated_monthly_savings", "timestamp"
            ])
            writer.writeheader()
    
    conn.close()
    return len(rows), csv_file

def export_savings_estimates():
    """Export savings estimates to CSV"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT total_current_monthly_cost, estimated_optimized_monthly_cost, 
               estimated_monthly_savings, timestamp
        FROM savings_estimates
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    csv_file = os.path.join(EXPORT_DIR, "savings_estimates.csv")
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        else:
            writer = csv.DictWriter(f, fieldnames=[
                "total_current_monthly_cost", "estimated_optimized_monthly_cost", 
                "estimated_monthly_savings", "timestamp"
            ])
            writer.writeheader()
    
    conn.close()
    return len(rows), csv_file

if __name__ == "__main__":
    print("=" * 60)
    print("CLOUD COST OPTIMIZER - DATA EXPORT")
    print("=" * 60)
    print(f"\n📊 Exporting data from: {DB_FILE}\n")
    
    try:
        # Export all data
        metric_count, metrics_file = export_resource_metrics()
        cost_count, costs_file = export_cost_records()
        rec_count, rec_file = export_recommendations()
        savings_count, savings_file = export_savings_estimates()
        
        print(f"✅ Resource Metrics:     {metric_count} records → {metrics_file}")
        print(f"✅ Cost Records:         {cost_count} records → {costs_file}")
        print(f"✅ Recommendations:      {rec_count} records → {rec_file}")
        print(f"✅ Savings Estimates:    {savings_count} records → {savings_file}")
        
        print(f"\n📁 All files exported to: {os.path.abspath(EXPORT_DIR)}/")
        print("\n💡 Use these CSV files with Power BI for visualization!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
