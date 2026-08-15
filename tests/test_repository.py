from datetime import datetime
from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from collector.azure_client import extract_metric_name
from database.db import Base
from database.models import CostRecord, ResourceMetric


def test_extract_metric_name_handles_string_and_localized_value():
    assert extract_metric_name(SimpleNamespace(name="UsedCapacity")) == "UsedCapacity"
    assert (
        extract_metric_name(
            SimpleNamespace(
                name=SimpleNamespace(localized_value="Used Capacity", value="UsedCapacity")
            )
        )
        == "Used Capacity"
    )


def test_sqlite_in_memory_database():
    engine = create_engine("sqlite:///:memory:", future=True)
    SessionLocal = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        metric = ResourceMetric(
            resource_id="test-resource",
            resource_name="test-vm",
            resource_type="Microsoft.Compute/virtualMachines",
            subscription_id="sub-123",
            cpu_utilization=5.5,
            status="running",
        )
        session.add(metric)
        session.commit()

        cost = CostRecord(
            subscription_id="sub-123",
            service_name="Virtual Machines",
            cost_amount=123.45,
            currency="USD",
            period_start=datetime(2024, 1, 1, 0, 0, 0),
            period_end=datetime(2024, 1, 31, 23, 59, 59),
        )
        session.add(cost)
        session.commit()

        assert session.query(ResourceMetric).count() == 1
        assert session.query(CostRecord).count() == 1
