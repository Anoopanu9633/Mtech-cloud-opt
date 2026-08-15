import csv
from datetime import datetime
from pathlib import Path

export_dir = Path("exports")
export_dir.mkdir(exist_ok=True)

SUBSCRIPTIONS = [
    "b918d096-c18b-4010-b5e2-28e636944fe8",
    "d123e456-f78a-9012-b345-c678d9012345",
    "a987b654-c32d-2109-e876-f543a2109876",
]
RESOURCE_GROUPS = ["prod", "dev", "test", "analytics", "infra", "shared"]
RESOURCE_TYPES = [
    ("Microsoft.Compute/virtualMachines", "vm", "compute"),
    ("Microsoft.Compute/disks", "disk", "storage"),
    ("Microsoft.Storage/storageAccounts", "storage", "storage"),
    ("Microsoft.Network/publicIPAddresses", "pip", "network"),
    ("Microsoft.Network/networkInterfaces", "nic", "network"),
    ("Microsoft.Network/networkSecurityGroups", "nsg", "network"),
    ("Microsoft.Network/virtualNetworks", "vnet", "network"),
    ("Microsoft.ContainerService/managedClusters", "aks", "kubernetes"),
    ("Microsoft.ContainerService/managedClusters/agentPools", "aks-nodepool", "kubernetes"),
    ("Microsoft.Storage/storageAccounts/blobServices/containers", "pvc", "storage"),
]

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cost_rows = []
for subscription in SUBSCRIPTIONS:
    for month in range(1, 9):
        cost_rows.append(
            {
                "subscription_id": subscription,
                "service_name": "Virtual Machines",
                "cost_amount": f"{850.50 + month * 23 + (SUBSCRIPTIONS.index(subscription) * 30):.2f}",
                "currency": "USD",
                "period_start": f"2026-{month:02d}-01 00:00:00",
                "period_end": f"2026-{month:02d}-28 23:59:59",
                "timestamp": now,
            }
        )
        cost_rows.append(
            {
                "subscription_id": subscription,
                "service_name": "Storage Accounts",
                "cost_amount": f"{320.10 + month * 6 + (SUBSCRIPTIONS.index(subscription) * 10):.2f}",
                "currency": "USD",
                "period_start": f"2026-{month:02d}-01 00:00:00",
                "period_end": f"2026-{month:02d}-28 23:59:59",
                "timestamp": now,
            }
        )
        cost_rows.append(
            {
                "subscription_id": subscription,
                "service_name": "Azure Kubernetes Service",
                "cost_amount": f"{550.00 + month * 15 + (SUBSCRIPTIONS.index(subscription) * 12):.2f}",
                "currency": "USD",
                "period_start": f"2026-{month:02d}-01 00:00:00",
                "period_end": f"2026-{month:02d}-28 23:59:59",
                "timestamp": now,
            }
        )

metric_rows = []
recommendation_rows = []
for index in range(1, 61):
    resource_type, prefix, category = RESOURCE_TYPES[index % len(RESOURCE_TYPES)]
    resource_group = RESOURCE_GROUPS[index % len(RESOURCE_GROUPS)]
    subscription = SUBSCRIPTIONS[index % len(SUBSCRIPTIONS)]
    resource_name = f"{prefix}-{resource_group}-{index:02d}"

    if resource_type == "Microsoft.ContainerService/managedClusters":
        resource_id = (
            f"/subscriptions/{subscription}/resourceGroups/{resource_group}"
            f"/providers/{resource_type}/{resource_name}"
        )
        cpu_utilization = ""
        disk_read_bytes = "0.0"
        disk_write_bytes = "0.0"
        storage_used = "0.0"
        status = "running"
        node_count = 3 + (index % 4)
        metric_rows.append(
            {
                "resource_id": resource_id,
                "resource_name": resource_name,
                "resource_type": resource_type,
                "cpu_utilization": "",
                "disk_read_bytes": disk_read_bytes,
                "disk_write_bytes": disk_write_bytes,
                "storage_used_gb": storage_used,
                "status": status,
                "timestamp": now,
            }
        )
        rec_type = "Kubernetes Cluster Review"
        rec_message = f"Review AKS cluster {resource_name} for node sizing and cost efficiency."
        rec_savings = f"{40.0 + index * 1.5:.2f}"

    elif resource_type == "Microsoft.ContainerService/managedClusters/agentPools":
        resource_id = (
            f"/subscriptions/{subscription}/resourceGroups/{resource_group}"
            f"/providers/Microsoft.ContainerService/managedClusters/aks-{resource_group}-01/agentPools/{resource_name}"
        )
        cpu_utilization = f"{15 + index % 60:.1f}"
        disk_read_bytes = f"{(index * 1100000) % 18000000:.1f}"
        disk_write_bytes = f"{(index * 900000) % 14000000:.1f}"
        storage_used = f"{80 + (index * 10) % 320:.1f}"
        status = "running"
        metric_rows.append(
            {
                "resource_id": resource_id,
                "resource_name": resource_name,
                "resource_type": resource_type,
                "cpu_utilization": cpu_utilization,
                "disk_read_bytes": disk_read_bytes,
                "disk_write_bytes": disk_write_bytes,
                "storage_used_gb": storage_used,
                "status": status,
                "timestamp": now,
            }
        )
        rec_type = "Kubernetes Node Pool Optimization"
        rec_message = "Consider scaling this AKS node pool based on utilization and workload requirements."
        rec_savings = f"{22.0 + index * 1.0:.2f}"

    elif resource_type == "Microsoft.Storage/storageAccounts/blobServices/containers":
        resource_id = (
            f"/subscriptions/{subscription}/resourceGroups/{resource_group}"
            f"/providers/{resource_type}/{resource_name}"
        )
        cpu_utilization = ""
        disk_read_bytes = f"{(index * 400000) % 14000000:.1f}"
        disk_write_bytes = f"{(index * 220000) % 12000000:.1f}"
        storage_used = f"{50 + (index * 22) % 600:.1f}"
        status = "bound" if index % 2 == 0 else "available"
        metric_rows.append(
            {
                "resource_id": resource_id,
                "resource_name": resource_name,
                "resource_type": resource_type,
                "cpu_utilization": cpu_utilization,
                "disk_read_bytes": disk_read_bytes,
                "disk_write_bytes": disk_write_bytes,
                "storage_used_gb": storage_used,
                "status": status,
                "timestamp": now,
            }
        )
        rec_type = "Kubernetes PVC Review"
        rec_message = "Evaluate this PVC-like storage container for retention and tiering optimization."
        rec_savings = f"{12.0 + index * 0.8:.2f}"

    else:
        resource_id = (
            f"/subscriptions/{subscription}/resourceGroups/{resource_group}"
            f"/providers/{resource_type}/{resource_name}"
        )
        if resource_type == "Microsoft.Compute/virtualMachines":
            cpu_utilization = f"{(index * 3.7) % 62 + 5:.1f}"
            status = "running" if index % 6 != 0 else "deallocated"
            storage_used = f"{64 + (index * 5) % 256:.1f}"
            disk_read_bytes = f"{(index * 1800000) % 15000000:.1f}"
            disk_write_bytes = f"{(index * 900000) % 9000000:.1f}"
            rec_type = "CPU Underutilized" if float(cpu_utilization) < 20 else "Right-size VM"
            rec_message = (
                "Consider resizing or shutting down this VM because its CPU utilization is consistently low."
                if float(cpu_utilization) < 20
                else "This VM is a good candidate for a smaller instance type to reduce cost."
            )
            rec_savings = f"{20.0 + index * 1.8:.2f}"
        elif resource_type == "Microsoft.Compute/disks":
            cpu_utilization = ""
            status = "unattached" if index % 4 == 0 else "attached"
            storage_used = f"{120 + (index * 12) % 650:.1f}"
            disk_read_bytes = "0.0" if status == "unattached" else f"{(index * 2100000) % 12500000:.1f}"
            disk_write_bytes = "0.0" if status == "unattached" else f"{(index * 1400000) % 10000000:.1f}"
            rec_type = "Unattached Disk" if status == "unattached" else "Low Activity Disk"
            rec_message = (
                "This disk appears unattached and can be deleted or archived to reduce cost."
                if status == "unattached"
                else "This disk has little IO activity and could be archived or downsized."
            )
            rec_savings = f"{8.0 + index * 0.7:.2f}"
        elif resource_type == "Microsoft.Storage/storageAccounts":
            cpu_utilization = ""
            status = "active"
            storage_used = f"{200 + (index * 18) % 1400:.1f}"
            disk_read_bytes = f"{(index * 2900000) % 16000000:.1f}"
            disk_write_bytes = f"{(index * 1700000) % 13000000:.1f}"
            rec_type = "Storage Tiering Opportunity"
            rec_message = "Consider moving cold storage data to a lower-cost tier."
            rec_savings = f"{28.0 + index * 1.2:.2f}"
        elif resource_type == "Microsoft.Network/publicIPAddresses":
            cpu_utilization = ""
            status = "unused" if index % 2 == 0 else "active"
            storage_used = "0.0"
            disk_read_bytes = "0.0"
            disk_write_bytes = "0.0"
            rec_type = "Unused Public IP" if status == "unused" else "Review Public IP Usage"
            rec_message = (
                "This public IP is not in use and can be released."
                if status == "unused"
                else "Review this public IP address to confirm it is still required."
            )
            rec_savings = f"{5.0 + index * 0.4:.2f}"
        elif resource_type == "Microsoft.Network/networkInterfaces":
            cpu_utilization = ""
            status = "inactive" if index % 4 == 0 else "active"
            storage_used = "0.0"
            disk_read_bytes = "0.0"
            disk_write_bytes = "0.0"
            rec_type = "Unused Network Interface"
            rec_message = "This network interface appears inactive and may be removed if no longer required."
            rec_savings = f"{7.0 + index * 0.35:.2f}"
        elif resource_type == "Microsoft.Network/networkSecurityGroups":
            cpu_utilization = ""
            status = "active"
            storage_used = "0.0"
            disk_read_bytes = "0.0"
            disk_write_bytes = "0.0"
            rec_type = "Network Security Review"
            rec_message = "Review this NSG for rules that could be consolidated or simplified."
            rec_savings = f"{10.0 + index * 0.5:.2f}"
        elif resource_type == "Microsoft.Network/virtualNetworks":
            cpu_utilization = ""
            status = "active"
            storage_used = "0.0"
            disk_read_bytes = "0.0"
            disk_write_bytes = "0.0"
            rec_type = "Virtual Network Review"
            rec_message = "This VNet can be reviewed for subnet consolidation and cost efficiency."
            rec_savings = f"{9.0 + index * 0.45:.2f}"
        else:
            cpu_utilization = ""
            status = "active"
            storage_used = "0.0"
            disk_read_bytes = "0.0"
            disk_write_bytes = "0.0"
            rec_type = "Review Resource Configuration"
            rec_message = "Review this resource for cost optimization opportunities."
            rec_savings = f"{10.0 + index * 0.6:.2f}"

        metric_rows.append(
            {
                "resource_id": resource_id,
                "resource_name": resource_name,
                "resource_type": resource_type,
                "cpu_utilization": cpu_utilization,
                "disk_read_bytes": disk_read_bytes,
                "disk_write_bytes": disk_write_bytes,
                "storage_used_gb": storage_used,
                "status": status,
                "timestamp": now,
            }
        )

    recommendation_rows.append(
        {
            "resource_id": resource_id,
            "resource_name": resource_name,
            "recommendation_type": rec_type,
            "message": rec_message,
            "estimated_monthly_savings": rec_savings,
            "timestamp": now,
        }
    )

savings_rows = []
for month in range(1, 13):
    current_cost = 1400.0 + month * 25.0
    optimized_cost = current_cost - (20.0 + month * 5.0)
    savings_rows.append(
        {
            "total_current_monthly_cost": f"{current_cost:.2f}",
            "estimated_optimized_monthly_cost": f"{optimized_cost:.2f}",
            "estimated_monthly_savings": f"{current_cost - optimized_cost:.2f}",
            "timestamp": now,
        }
    )

files = [
    (
        "cost_records.csv",
        ["subscription_id", "service_name", "cost_amount", "currency", "period_start", "period_end", "timestamp"],
        cost_rows,
    ),
    (
        "resource_metrics.csv",
        [
            "resource_id",
            "resource_name",
            "resource_type",
            "cpu_utilization",
            "disk_read_bytes",
            "disk_write_bytes",
            "storage_used_gb",
            "status",
            "timestamp",
        ],
        metric_rows,
    ),
    (
        "recommendations.csv",
        [
            "resource_id",
            "resource_name",
            "recommendation_type",
            "message",
            "estimated_monthly_savings",
            "timestamp",
        ],
        recommendation_rows,
    ),
    (
        "savings_estimates.csv",
        [
            "total_current_monthly_cost",
            "estimated_optimized_monthly_cost",
            "estimated_monthly_savings",
            "timestamp",
        ],
        savings_rows,
    ),
]

for filename, fieldnames, rows in files:
    target_path = export_dir / filename
    try:
        with open(target_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {target_path}")
    except PermissionError:
        fallback_path = export_dir / f"{filename}.new"
        with open(fallback_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Permission denied writing {target_path}; wrote to {fallback_path} instead")
