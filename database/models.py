from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ResourceMetric(Base):
    __tablename__ = "resource_metrics"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String(256), index=True, nullable=False)
    resource_name = Column(String(256), nullable=False)
    resource_type = Column(String(128), nullable=False)
    subscription_id = Column(String(128), nullable=True)
    region = Column(String(64), nullable=True)
    cpu_utilization = Column(Float, nullable=True)
    disk_read_bytes = Column(Float, nullable=True)
    disk_write_bytes = Column(Float, nullable=True)
    storage_used_gb = Column(Float, nullable=True)
    status = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(String(128), nullable=False)
    service_name = Column(String(256), nullable=True)
    cost_amount = Column(Float, nullable=False)
    currency = Column(String(16), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(String(256), nullable=False)
    resource_name = Column(String(256), nullable=False)
    recommendation_type = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    estimated_monthly_savings = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class SavingsEstimate(Base):
    __tablename__ = "savings_estimates"

    id = Column(Integer, primary_key=True, index=True)
    total_current_monthly_cost = Column(Float, nullable=False)
    estimated_optimized_monthly_cost = Column(Float, nullable=False)
    estimated_monthly_savings = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
