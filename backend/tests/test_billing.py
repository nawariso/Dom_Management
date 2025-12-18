from datetime import date
from decimal import Decimal

from backend.app.billing import calculate_tariff_charge, prorate_amount
from backend.app.models import Tariff


def test_proration_handles_room_move():
    amount = Decimal("100.00")
    period_start = date(2024, 1, 1)
    period_end = date(2024, 2, 1)
    # tenant moves out mid-cycle
    prorated = prorate_amount(amount, date(2024, 1, 10), date(2024, 1, 20), period_start, period_end)
    assert prorated == Decimal("32.26")


def test_tiered_tariff_charge():
    tariff = Tariff(
        name="Tiered",
        rate_per_unit=Decimal("6.00"),
        base_fee=Decimal("10.00"),
        currency="THB",
        effective_from=date.today(),
        tiers=[{"up_to": 50, "rate": 4.0}, {"up_to": 20, "rate": 5.0}],
    )
    charge = calculate_tariff_charge(Decimal("60"), tariff)
    assert charge == Decimal("310.00")
