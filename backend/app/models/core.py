from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base


class Dorm(Base):
    __tablename__ = "dorms"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(512), nullable=False)
    contact_email = Column(String(255), nullable=True)

    buildings = relationship("Building", back_populates="dorm")


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    dorm_id = Column(Integer, ForeignKey("dorms.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)

    dorm = relationship("Dorm", back_populates="buildings")
    floors = relationship("Floor", back_populates="building")

    __table_args__ = (UniqueConstraint("dorm_id", "name", name="uq_building_name_per_dorm"),)


class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    number = Column(Integer, nullable=False)

    building = relationship("Building", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")

    __table_args__ = (
        UniqueConstraint("building_id", "number", name="uq_floor_number_per_building"),
    )


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    floor_id = Column(Integer, ForeignKey("floors.id", ondelete="CASCADE"), nullable=False)
    number = Column(String(50), nullable=False)
    is_occupied = Column(Boolean, default=False, nullable=False)

    floor = relationship("Floor", back_populates="rooms")
    tenant = relationship("Tenant", back_populates="room", uselist=False)
    meters = relationship("Meter", back_populates="room")

    __table_args__ = (UniqueConstraint("floor_id", "number", name="uq_room_number_per_floor"),)


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    move_in = Column(Date, nullable=True)
    move_out = Column(Date, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    room = relationship("Room", back_populates="tenant")
    invoices = relationship("Invoice", back_populates="tenant")
    subscriptions = relationship("Subscription", back_populates="tenant")


class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    serial_number = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)

    room = relationship("Room", back_populates="meters")
    usage_records = relationship("UsageRecord", back_populates="meter")

    __table_args__ = (
        CheckConstraint("type in ('water','electric')", name="ck_meter_type"),
    )


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    rate_per_unit = Column(Numeric(10, 4), nullable=False)
    base_fee = Column(Numeric(10, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="THB")
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    tiers = Column(JSON, nullable=True)

    usage_records = relationship("UsageRecord", back_populates="tariff")


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True)
    meter_id = Column(Integer, ForeignKey("meters.id", ondelete="CASCADE"), nullable=False)
    tariff_id = Column(Integer, ForeignKey("tariffs.id", ondelete="SET NULL"), nullable=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    consumption = Column(Float, nullable=False)
    cost = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    meter = relationship("Meter", back_populates="usage_records")
    tariff = relationship("Tariff", back_populates="usage_records")

    __table_args__ = (
        UniqueConstraint("meter_id", "period_start", "period_end", name="uq_meter_period"),
        CheckConstraint("consumption >= 0", name="ck_consumption_positive"),
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(
        Enum("pending", "paid", "overdue", "cancelled", name="invoice_status"),
        nullable=False,
        default="pending",
    )
    due_date = Column(Date, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("Tenant", back_populates="invoices")
    room = relationship("Room")
    payments = relationship("Payment", back_populates="invoice")

    __table_args__ = (
        UniqueConstraint("tenant_id", "period_start", "period_end", name="uq_invoice_period_per_tenant"),
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(
        Enum("initiated", "succeeded", "failed", name="payment_status"), nullable=False, default="initiated"
    )
    transaction_ref = Column(String(255), nullable=False, unique=True)
    method = Column(String(50), nullable=True)
    paid_at = Column(DateTime, nullable=True)

    invoice = relationship("Invoice", back_populates="payments")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    plan_name = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    interval = Column(String(50), nullable=False)
    next_billing_date = Column(Date, nullable=False)
    status = Column(
        Enum("active", "past_due", "canceled", "paused", name="subscription_status"),
        nullable=False,
        default="active",
    )
    retry_count = Column(Integer, default=0, nullable=False)

    tenant = relationship("Tenant", back_populates="subscriptions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    actor = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (Index("idx_audit_entity", "entity_type", "entity_id"),)


__all__ = [
    "Dorm",
    "Building",
    "Floor",
    "Room",
    "Tenant",
    "Meter",
    "UsageRecord",
    "Tariff",
    "Invoice",
    "Payment",
    "Subscription",
    "AuditLog",
]
