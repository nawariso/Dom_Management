from datetime import datetime
from typing import Optional

from .base import SchemaBase


class AuthRequest(SchemaBase):
    email: str
    password: str


class AuthResponse(SchemaBase):
    access_token: str
    token_type: str = "bearer"
    role: str


class Tenant(SchemaBase):
    id: int
    name: str
    timezone: str


class Room(SchemaBase):
    id: int
    name: str
    tenant_id: int


class Meter(SchemaBase):
    id: int
    serial_number: str
    room_id: int


class UsageRecord(SchemaBase):
    id: int
    meter_id: int
    consumed_kwh: float
    recorded_at: datetime


class Invoice(SchemaBase):
    id: int
    tenant_id: int
    amount_due: float
    due_date: datetime
    status: str


class Payment(SchemaBase):
    id: int
    invoice_id: int
    amount: float
    processed_at: datetime
    status: str
    provider_reference: Optional[str] = None
