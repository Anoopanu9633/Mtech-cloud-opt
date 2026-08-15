from dotenv import load_dotenv
load_dotenv()

from database.db import SessionLocal, init_db
from collector.data_fetcher import AzureDataFetcher
from export_data import (
    export_cost_records,
    export_recommendations,
    export_resource_metrics,
    export_savings_estimates,
)


def main():
    init_db()
    db = SessionLocal()
    fetcher = AzureDataFetcher()

    print('\n== Resource discovery ==')
    resources = fetcher.fetch_resources()
    print(f'Found {len(resources)} resources')
    for r in resources:
        print(' -', getattr(r, 'id', None), getattr(r, 'name', None), getattr(r, 'type', None))

    print('\n== Resource metrics (saved) ==')
    metrics = fetcher.fetch_resource_metrics(db)
    print(f'Returned {len(metrics)} metric records')
    for m in metrics:
        print(m)

    print('\n== Cost records (saved) ==')
    costs = fetcher.fetch_cost_records(db)
    print(f'Returned {len(costs)} cost records')
    for c in costs:
        print(c)

    db.close()

    print('\n== Exporting CSV files ==')
    metric_count, metrics_file = export_resource_metrics()
    cost_count, costs_file = export_cost_records()
    rec_count, rec_file = export_recommendations()
    savings_count, savings_file = export_savings_estimates()
    print(f'Exported {metric_count} metric rows to {metrics_file}')
    print(f'Exported {cost_count} cost rows to {costs_file}')
    print(f'Exported {rec_count} recommendation rows to {rec_file}')
    print(f'Exported {savings_count} savings rows to {savings_file}')


if __name__ == '__main__':
    main()
