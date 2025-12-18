from datetime import date, timedelta

from backend.app.models import (
    Building,
    Dorm,
    Floor,
    Invoice,
    Room,
    Subscription,
    Tenant,
    UsageRecord,
)
from backend.app.repositories import (
    BuildingRepository,
    DormRepository,
    FloorRepository,
    InvoiceRepository,
    RoomRepository,
    SubscriptionRepository,
    TenantRepository,
    UsageRecordRepository,
)


def seed_basic_graph(session):
    dorm = Dorm(name="Dorm Alpha", address="Somewhere")
    building = Building(name="A", dorm=dorm)
    floor = Floor(number=1, building=building)
    room1 = Room(number="101", floor=floor, is_occupied=False)
    room2 = Room(number="102", floor=floor, is_occupied=True)
    tenant = Tenant(name="Alice", email="alice@example.com", room=room2, move_in=date.today())
    session.add_all([dorm, building, floor, room1, room2, tenant])
    session.flush()
    return dorm, building, floor, room1, room2, tenant


def test_room_and_tenant_repositories(db_session):
    dorm, building, floor, room1, room2, tenant = seed_basic_graph(db_session)

    dorm_repo = DormRepository(db_session)
    building_repo = BuildingRepository(db_session)
    floor_repo = FloorRepository(db_session)
    room_repo = RoomRepository(db_session)
    tenant_repo = TenantRepository(db_session)

    assert dorm_repo.find_by_name("Dorm Alpha") == dorm
    assert building_repo.list_by_dorm(dorm.id) == [building]
    assert floor_repo.list_by_building(building.id) == [floor]

    available = room_repo.find_available_on_floor(floor.id)
    assert available == room1

    active_tenants = tenant_repo.active_between(date.today() - timedelta(days=1), date.today())
    assert tenant in active_tenants
    assert tenant_repo.get_by_email("alice@example.com") == tenant


def test_usage_invoice_and_subscription_repositories(db_session):
    dorm, building, floor, room1, room2, tenant = seed_basic_graph(db_session)

    usage_repo = UsageRecordRepository(db_session)
    invoice_repo = InvoiceRepository(db_session)
    subscription_repo = SubscriptionRepository(db_session)

    usage1 = UsageRecord(
        meter_id=1,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        consumption=10,
        cost=100,
    )
    usage2 = UsageRecord(
        meter_id=1,
        period_start=date(2024, 2, 1),
        period_end=date(2024, 2, 29),
        consumption=12,
        cost=120,
    )
    db_session.add_all([usage1, usage2])
    db_session.flush()

    assert usage_repo.for_meter(1) == [usage1, usage2]

    invoice_pending = Invoice(
        tenant=tenant,
        room=room2,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        total_amount=100,
        status="pending",
    )
    invoice_paid = Invoice(
        tenant=tenant,
        room=room2,
        period_start=date(2024, 2, 1),
        period_end=date(2024, 2, 29),
        total_amount=120,
        status="paid",
    )
    db_session.add_all([invoice_pending, invoice_paid])
    db_session.flush()

    unpaid = invoice_repo.unpaid_for_tenant(tenant.id)
    assert unpaid == [invoice_pending]

    subscription_active = Subscription(
        tenant=tenant,
        plan_name="Standard",
        amount=500,
        interval="monthly",
        next_billing_date=date.today(),
        status="active",
    )
    subscription_delinquent = Subscription(
        tenant=tenant,
        plan_name="Standard",
        amount=500,
        interval="monthly",
        next_billing_date=date.today() - timedelta(days=5),
        status="past_due",
        retry_count=3,
    )
    db_session.add_all([subscription_active, subscription_delinquent])
    db_session.flush()

    due = subscription_repo.due_for_billing(date.today())
    assert subscription_active in due
    assert subscription_delinquent not in due

    subscription_repo.mark_retry(subscription_active)
    assert subscription_active.retry_count == 1
    assert subscription_active.status == "active"
