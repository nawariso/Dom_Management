from datetime import date
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models import (
    Building,
    Dorm,
    Floor,
    Invoice,
    Payment,
    Room,
    Subscription,
    Tenant,
    UsageRecord,
)
from .base import Repository


class DormRepository(Repository[Dorm]):
    def __init__(self, session: Session):
        super().__init__(session, Dorm)

    def find_by_name(self, name: str) -> Optional[Dorm]:
        return self.session.query(Dorm).filter(Dorm.name == name).one_or_none()


class BuildingRepository(Repository[Building]):
    def __init__(self, session: Session):
        super().__init__(session, Building)

    def list_by_dorm(self, dorm_id: int) -> List[Building]:
        return list(self.session.query(Building).filter(Building.dorm_id == dorm_id))


class FloorRepository(Repository[Floor]):
    def __init__(self, session: Session):
        super().__init__(session, Floor)

    def list_by_building(self, building_id: int) -> List[Floor]:
        return list(self.session.query(Floor).filter(Floor.building_id == building_id))


class RoomRepository(Repository[Room]):
    def __init__(self, session: Session):
        super().__init__(session, Room)

    def find_available_on_floor(self, floor_id: int) -> Optional[Room]:
        return (
            self.session.query(Room)
            .filter(Room.floor_id == floor_id, Room.is_occupied.is_(False))
            .order_by(Room.number)
            .first()
        )


class TenantRepository(Repository[Tenant]):
    def __init__(self, session: Session):
        super().__init__(session, Tenant)

    def get_by_email(self, email: str) -> Optional[Tenant]:
        return self.session.query(Tenant).filter(Tenant.email == email).one_or_none()

    def active_between(self, start: date, end: date) -> List[Tenant]:
        return list(
            self.session.query(Tenant)
            .filter(
                Tenant.active.is_(True),
                or_(Tenant.move_out.is_(None), Tenant.move_out >= start),
                or_(Tenant.move_in.is_(None), Tenant.move_in <= end),
            )
            .all()
        )


class UsageRecordRepository(Repository[UsageRecord]):
    def __init__(self, session: Session):
        super().__init__(session, UsageRecord)

    def for_meter(self, meter_id: int) -> List[UsageRecord]:
        return list(
            self.session.query(UsageRecord)
            .filter(UsageRecord.meter_id == meter_id)
            .order_by(UsageRecord.period_start)
            .all()
        )


class InvoiceRepository(Repository[Invoice]):
    def __init__(self, session: Session):
        super().__init__(session, Invoice)

    def unpaid_for_tenant(self, tenant_id: int) -> List[Invoice]:
        return list(
            self.session.query(Invoice)
            .filter(Invoice.tenant_id == tenant_id, Invoice.status != "paid")
            .order_by(Invoice.due_date)
            .all()
        )


class PaymentRepository(Repository[Payment]):
    def __init__(self, session: Session):
        super().__init__(session, Payment)

    def for_invoice(self, invoice_id: int) -> List[Payment]:
        return list(
            self.session.query(Payment)
            .filter(Payment.invoice_id == invoice_id)
            .order_by(Payment.created_at)
            .all()
        )


class SubscriptionRepository(Repository[Subscription]):
    def __init__(self, session: Session):
        super().__init__(session, Subscription)

    def due_for_billing(self, as_of: date) -> List[Subscription]:
        return list(
            self.session.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.next_billing_date <= as_of,
                Subscription.retry_count < 3,
            )
            .all()
        )

    def mark_retry(self, subscription: Subscription) -> Subscription:
        subscription.retry_count += 1
        if subscription.retry_count >= 3:
            subscription.status = "past_due"
        self.session.add(subscription)
        return subscription
