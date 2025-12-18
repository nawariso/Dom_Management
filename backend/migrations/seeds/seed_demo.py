from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.models import (
    Base,
    AuditLog,
    Building,
    Dorm,
    Floor,
    Invoice,
    Meter,
    Room,
    Tariff,
    Tenant,
    UsageRecord,
)

ENGINE_URL = "sqlite:///./dorm.db"


def seed_demo_data() -> None:
    engine = create_engine(ENGINE_URL, future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        dorm = Dorm(name="Siam Residence", address="123 Main", contact_email="owner@example.com")
        building = Building(name="A", dorm=dorm)
        floor = Floor(number=1, building=building)
        room = Room(number="101", floor=floor, is_occupied=True)
        tenant = Tenant(name="Alice", email="alice@example.com", room=room, move_in=date.today())
        meter = Meter(type="electric", serial_number="ELEC-001", room=room)
        tariff = Tariff(
            name="Default",
            rate_per_unit=Decimal("5.50"),
            base_fee=Decimal("50"),
            currency="THB",
            effective_from=date.today(),
            tiers=[{"up_to": 50, "rate": 4.5}, {"up_to": 100, "rate": 5.0}],
        )
        usage = UsageRecord(
            meter=meter,
            tariff=tariff,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            consumption=42.0,
            cost=Decimal("0.00"),
        )
        session.add_all([dorm, building, floor, room, tenant, meter, tariff, usage])
        session.commit()

        invoice = Invoice(
            tenant=tenant,
            room=room,
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            total_amount=Decimal("0.00"),
            status="pending",
            due_date=date(2024, 2, 7),
        )
        session.add(invoice)
        session.flush()

        log = AuditLog(
            actor="system",
            action="seed",
            entity_type="invoice",
            entity_id=invoice.id,
            metadata={"note": "Seed data created"},
        )
        session.add(log)
        session.commit()


if __name__ == "__main__":
    seed_demo_data()
