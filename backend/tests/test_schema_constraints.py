from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.models import Building, Dorm, Floor, Meter, Room, Tariff, Tenant


def test_unique_meter_serial(db_session):
    dorm = Dorm(name="Dorm A", address="A")
    building = Building(name="B1", dorm=dorm)
    floor = Floor(number=1, building=building)
    room = Room(number="101", floor=floor)
    tariff = Tariff(
        name="T1",
        rate_per_unit=1,
        base_fee=0,
        currency="THB",
        effective_from=date.today(),
    )
    db_session.add_all([dorm, building, floor, room, tariff])
    db_session.flush()

    meter1 = Meter(type="electric", serial_number="DUP", room=room)
    meter2 = Meter(type="electric", serial_number="DUP", room=room)
    db_session.add_all([meter1, meter2])

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_unique_tenant_email(db_session):
    tenant1 = Tenant(name="Alice", email="alice@example.com")
    tenant2 = Tenant(name="Bob", email="alice@example.com")
    db_session.add_all([tenant1, tenant2])
    with pytest.raises(IntegrityError):
        db_session.commit()
